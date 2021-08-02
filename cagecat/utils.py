"""Utility module to support the CAGECAT web service

Author: Matthias van den Belt
"""
# package imports
import os
import random
from rq.registry import StartedJobRegistry
from datetime import datetime
import smtplib
import ssl

# own project imports
from cagecat.models import Job, Statistic
from config_files.config import EMAIL
import cagecat.const as const

# typing imports
import werkzeug.datastructures, werkzeug.utils
import rq
import redis
import typing as t
from flask_sqlalchemy import SQLAlchemy

# create final variables
CLUST_NUMBER_PATTERN_W_SCORE = r"\(Cluster (\d+), score: \d+\.\d+\)"
CLUST_NUMBER_PATTERN_WITHOUT_SCORE = r"\(Cluster (\d+)"
CLUST_NUMBER_PATTERN_W_CLINKER_SCORE = r"\(Cluster (\d+), \d+\.\d+ score\)"

JOBS_DIR = os.path.join("cagecat", "jobs")
FOLDERS_TO_CREATE = ["uploads", "results", "logs"]
PATTERN = r"[ {]'([a-zA-Z]+)': '(\w*?)'"


### Function definitions
def generate_job_id(id_len: int = 15) -> str:
    # TODO: would: could make length shorter
    """Generates a numeric job ID with each 4th character being a letter

    Input:
        - id_len, int: length of the job ID to be generated

    Output:
        - job_id, str: a randomly generated job ID
    """
    characters = []
    existing_job = 0

    while existing_job is not None:
        for i in range(id_len):
            if i % 4 == 0:
                min_ord, max_ord = 65, 90
            else:
                min_ord, max_ord = 48, 57

            characters.append(chr(random.randint(min_ord, max_ord)))

        job_id = "".join(characters)
        existing_job = fetch_job_from_db(job_id)
        # existing_job becomes None if no such job exists

    return job_id


def save_file(file_obj: werkzeug.datastructures.FileStorage,
              job_id: str) -> str:
    """Saves file in specific job uploads folder using the provided filename

    Input:
        - file_obj: via HTTP form user submitted file. Given like:
            request.form[filename]
        - job_id, str: ID corresponding to the job the function is called for

    Output:
        - file_path, str: path where the file has been saved
    """
    fn = werkzeug.utils.secure_filename(file_obj.filename)
    if fn:

        file_path = os.path.join(f"{JOBS_DIR}", job_id,
                                 "uploads", fn)
        file_obj.save(file_path)
    else:
        raise IOError('Securing filename led to an empty filename')

    return file_path


def get_server_info(q: rq.Queue, redis_conn: redis.Redis) \
        -> t.Dict[str, t.Union[str, int]]:
    """Returns current server statistics and information

    Input:
        - q, rq.Queue: connection to queue of jobs waiting to be executed
        - redis_conn, redis.Redis: instance of Redis server. Used to connect
            to Redis

    Output:
        - dict: info about the current status of the server and queued
            or running jobs
    """
    # TODO: would, optimization: maybe we can instantiate this registry once instead of every time

    start_registry = StartedJobRegistry('default', connection=redis_conn)
    # above registry has the jobs in it which have been started, but are not
    # finished yet: running jobs.
    running = len(start_registry)

    return {"server_status": 'idle' if running == 0 else 'running',
            "queued": len(q),
            "running": running,
            "completed": Statistic.query.filter_by(
                name="finished").first().count}


def create_directories(job_id: str) -> None:
    """Creates directories for a job ID

    Input:
        - job_id: ID corresponding to the job the function is called for

    Output:
        - None
        - Created directories
    """
    base_path = os.path.join(JOBS_DIR, job_id)

    if not os.path.exists(base_path): # directories are attempted to
        # be created again when jobs depending on each other are executed
        os.mkdir(base_path)
        for folder in FOLDERS_TO_CREATE:
            os.mkdir(os.path.join(base_path, folder))
    else:
        print(f"Directory {base_path} already exists. Skipped")


def add_time_to_db(job_id: str, time_type: str, db: SQLAlchemy) -> None:
    """Adds timestamp to job entry with given ID in SQL database

    Input:
        - job_id: ID corresponding to the job the function is called for
        - time_type: column in the SQL table to which a timestamp should be
            added. Available options are: ["start", "finish"]
        - db: SQL database connection with the Flask application

    Output:
        - None
        - Stored time at given column in the SQL database
    """
    job = fetch_job_from_db(job_id)

    if time_type == "start":
        job.start_time = datetime.utcnow()
    elif time_type == "finish":
        job.finish_time = datetime.utcnow()
    else:
        raise IOError("Invalid time type")

    db.session.commit()


def mutate_status(job_id: str, stage: str, db: SQLAlchemy,
                  return_code: t.Optional[int] = None) -> None:
    """Mutates status of job entry with given ID in SQL database

    Input:
        - job_id: ID corresponding to the job the function is called for
        - stage: stage the job has entered. Available options are:
            ["start", "finish"]
        - db: SQL database connection with the Flask application
        - return_code: exit code of the command ran. 0 indicates command
            execution without errors

    Output:
        - None
        - Mutated job status in the SQL database

    Raises:
        - IOError: when the given stage is invalid
    """
    job = fetch_job_from_db(job_id)

    if stage == "start":
        new_status = "running"
    elif stage == "finish":
        if return_code is None:
            raise IOError("Return code should be provided")
        elif not return_code:  # return code of 0
            new_status = "finished"
        else:
            new_status = "failed"

        Statistic.query.filter_by(name=new_status).first().count += 1

    else:
        raise IOError("Invalid stage")

    job.status = new_status
    db.session.commit()


def save_settings(options: werkzeug.datastructures.ImmutableMultiDict,
                  job_id: str) -> None:
    """Writes job settings to a file with which the job was submitted

    Input:
        - options: user submitted options (values) via HTTP form of front-end
        - job_id: ID corresponding to the job the function is called for

    Output:
        - None
        - New file with options written to it

    Function created for logging purposes. Writes to a file, which will be
    used by the [load_settings] function.
    """
    with open(f"{os.path.join(JOBS_DIR, job_id, 'logs', job_id)}"
              f"_options.txt", "w") as outf:

        for key, value in options.items():
            if type(value) == str:
                if "\r\n" in value:
                    value = ','.join(value.split('\r\n'))

            outf.write(f"{key},{value}\n")


def fetch_job_from_db(job_id: str) -> t.Optional[Job]:
    """Checks if a job with a specific job ID exists in the database

    Input:
        - job_id: ID of a job to search for

    Output:
        - Job instance if present in the database OR
        - None if no job with the given ID was found in the database
    """
    return Job.query.filter_by(id=job_id).first()


def check_valid_job(prev_job_id: str) -> None:
    """Checks if a submitted job, relying on a previous job is valid

    Input:
        - prev_job_id: ID of the user-submitted previous job

    Output:
        - None

    Raises:
        - NotImplementedError: when previous_job_id was not found in
            the database
    """
    if fetch_job_from_db(prev_job_id) is None:
        raise NotImplementedError("Unknown job ID. Template should be created")


def format_size(size: int) -> str:
    """Formats the size of a file into MB

    Input:
        - size: size of the a file in bytes

    Output:
        - formatted string showing the size of the file ..MB
    """
    return "%3.1f MB" % (size/1000000) if size is not None else size


def read_headers(job_id: str) -> t.List[str]:
    """Reads headers belonging to the search of a job ID

    Input:
        - job_id: id of the job for which the query headers are asked for

    Output:
        - headers: the query headers of this job ID
    """
    with open(os.path.join(JOBS_DIR, job_id, "logs", "query_headers.csv")) as outf:
        headers = outf.read().strip().split(",")

    return headers


def send_email(subject: str, message: str, receiving_email: str) -> None:
    """Send an email

    Input:
        - subject: subject of the email
        - message: body content of the email
        - receiving_email: e-mail address of the receiver

    Output:
        - None, sent emails
    """
    message = f"Subject: {subject}\n\n{message}\n{EMAIL['FOOTER_MSG']}"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(EMAIL['SMTP_SERVER'], EMAIL['PORT'], context=context) as server:
        server.login(EMAIL['SENDER_EMAIL'], EMAIL['PASSWORD'])
        server.sendmail(EMAIL['SENDER_EMAIL'], receiving_email, message)


def get_failure_reason(job_id: str, program: str) -> str:
    """Gets the user-friendly failure reason when a job has failed

    Input:
        - job_id: job id which has failed and the reason should be looked
            up for

    Output:
        - user-friendly failure reason
    """
    try:
        with open(os.path.join(JOBS_DIR, job_id,
                               "logs", f"{job_id}_{program}.log")) as inf:
            logs = inf.readlines()

        for l in logs:
            for fail in const.FAILURE_REASONS:
                if fail in l:
                    return const.FAILURE_REASONS[fail]
    except FileNotFoundError:
        return 'Command construction failed (no log file).'

    return 'Unknown failure reason.'
