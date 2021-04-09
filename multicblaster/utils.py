"""Utility module to support the multicblaster web service

Author: Matthias van den Belt
"""
import os
import random
from rq.registry import StartedJobRegistry
from multicblaster.models import Job, Statistic
from datetime import datetime
import re
import signal
import pickle

# typing imports
import werkzeug.datastructures
import rq
import redis
import typing as t
from flask_sqlalchemy import SQLAlchemy

# create final variables
CLUST_NUMBER_PATTERN = r"\(Cluster (\d+), score: \d+\.\d+\)"

JOBS_DIR = os.path.join("multicblaster", "jobs")
FOLDERS_TO_CREATE = ["uploads", "results", "logs"]
SUBMIT_URL = "/submit_job"
PATTERN = r"[ {]'([a-zA-Z]+)': '(\w*?)'"

# INVALID_JOB_COMBINATIONS = []
INVALID_JOB_COMBINATIONS = [("recompute", "recompute"),
                            ("gne", "gne"),
                            ("recompute", "gne"),
                            ("gne", "recompute")]

MODULES_CLUSTER_SELECTION = ["search", "recompute"]
# TODO: really check if above combinations are not valid, and document what
# kind of errors they produce

PRETTY_TRANSLATION = {"job_type": "Job type",
                      "inputType": "Input type",
                      "ncbiEntriesTextArea": "NCBI entries",
                      "searchPreviousType": "Previous session type",
                      "database_type": "Database",
                      "entrez_query": "Entrez query",
                      "max_hits": "Maximum hits",
                      "max_evalue": "Maximum e-value",
                      "min_identity": "Minimum % identity",
                      "min_query_coverage": "Minimum query coverage (%)",
                      "max_intergenic_gap": "Maximum intergenic gap",
                      "min_unique_query_hits": "Minimum unique query hits",
                      "min_hits_in_clusters": "Minimum hits in clusters",
                      "searchSumTableDelim": "Summary delimiter",
                      "searchSumTableDecimals": "Summary decimals",
                      "searchBinTableDelim": "Binary delimiter",
                      "searchBinTableDecimals": "Binary decimals",
                      "keyFunction": "Key function",
                      "sortClusters": "Sort clusters",
                      "generatePlot": "Generate plot",
                      "gnePreviousType": "Previous session type",
                      "requiredSequencesCheckbox": None,
                      "requiredSequences": "Required sequences",
                      "searchBinTableHideHeaders": "Binary hide headers",
                      "hitAttribute": "Hit attribute",
                      "searchSumTableHideHeaders": "Summary hide headers",
                      "searchEnteredJobId": "Previous job ID",
                      "gneEnteredJobId": "Previous job ID",
                      "gneSumTableDelim": "Summary delimiter",
                      "gneSumTableDecimals": "Summary decimals",
                      "gneSumTableHideHeaders": "Summary hide headers",
                      "max_intergenic_distance": "Maximum intergenic distance",
                      "sample_number": "Sample size",
                      "sampling_space": "Sampling space",
                      "prev_job_id": "Previous job ID",
                      "selectedQueries": "Selected queries",
                      "selectedOrganisms": "Selected organisms",
                      "selectedScaffolds": "Selected scaffolds",
                      "outputDelimiter": "Delimiter",
                      "downloadSeqs": "Download sequences",
                      "nameOnly": "Name only",
                      "clusterNumbers": "Selected clusters",
                      "clusterScoreThreshold": "Score threshold",
                      "prefix": "File prefix",
                      "format": "Output format",
                      "maxclusters": "Maximum clusters",
                      "selectedQuery": "Query",
                      "selectedReferenceCluster": "Reference cluster",
                      "selectedClustersToSearch": "Clusters to search in",
                      "clusterRadio": "Cluster radio",
                      "bitscore": "Bitscore",
                      "rescale": "Rescale",
                      "antismashFile": "antiSmash file:",
                      "evalue": "e-value"

                      # "selectedClusters":
                      }

FILE_POST_FUNCTION_ID_TRANS = {"create_database": "genomeFiles",
                               "calculate_neighbourhood": "outputFileName"
                               }

COMPRESSION_FORMATS = [".tar", ".tar.gz", ".gz", ".7z", ".zip", ".rar"]

TEST_PATH = ".."


def generate_job_id(id_len: int = 15) -> str:
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

    # TODO: should make filename safe (e.g. secure_filename function of Flask)
    """
    file_path = os.path.join(f"{JOBS_DIR}", job_id,
                             "uploads", file_obj.filename)
    file_obj.save(file_path)

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
    # TODO: maybe we can instantiate this registry once instead of every time

    start_registry = StartedJobRegistry('default', connection=redis_conn)
    # above registry has the jobs in it which have been started, but are not
    # finished yet: running jobs.
    queued = len(q)
    running = len(start_registry)

    if queued == 0:
        if running == 0:
            status = "idle"
        else:
            status = "running"
    else:
        status = "waiting"

    return {"server_status": status,
            "queued": queued,
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


def load_settings(job_id: str) -> t.Dict[str, str]:
    """Loads settings with which a job was submitted by a user from a file

    Input:
        - job_id: ID corresponding to the job the function is called for

    Output:
        - settings_dict: to be used when generating HTML. With the format
            {pretty_label_of_setting : submitted_value}

    Loads file written by the [save_settings] function
    """
    settings_dict = {}

    with open(os.path.join(JOBS_DIR, job_id, "logs",
                           f"{job_id}_options.txt")) as inf:
        settings = inf.readlines()

    rewritten_settings = {}
    for line in settings:
        splitted = line.strip().split(",")

        if len(splitted) == 2:
            rewritten_settings[splitted[0]] = splitted[1]
        elif len(splitted) > 2:
            rewritten_settings[splitted[0]] = ", ".join(splitted[1:])
        else:
            raise IOError("Invalid setting length")

    for key, value in rewritten_settings.items():
        label = PRETTY_TRANSLATION[key]

        if label is not None:
            settings_dict[label] = value

    return settings_dict


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
    print("Save settings: ")
    print(options)
    with open(f"{os.path.join(JOBS_DIR, job_id, 'logs', job_id)}"
              f"_options.txt", "w") as outf:
    # TODO: check if we can replace this with os.path.join(log_base, f"{job_id}_cmd.txt"), "w"
    #     outf.write(str(dict(options)))


        for key, value in options.items():
            if "\r\n" in value:
                value = ','.join(value.split('\r\n'))

            # new_val =
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


def check_valid_job(prev_job_id: str, job_type: str) -> None:
    """Checks if a submitted job, relying on a previous job is valid

    Input:
        - prev_job_id: ID of the user-submitted previous job
        - job_type: type of the submitted job e.g. "search" or "gne"

    Output: # TODO: might change into rendering templates
        - None

    Raises:
        - NotImplementedError: when previous_job_id was not found in
            the database
        - NotImplementedError: when the combination of the previous job type
            and the new job type is invalid (would cause multicblaster
            to crash)
    """
    if fetch_job_from_db(prev_job_id) is None:
        # TODO: create invalid job ID template
        # TODO: OR let JS check job ID on front-end
        raise NotImplementedError("Unknown job ID. Template should be created")
    if (fetch_job_from_db(prev_job_id).job_type, job_type) in \
            INVALID_JOB_COMBINATIONS:
        # TODO: should create template
        raise NotImplementedError(f"Invalid combinations of job types. Prev job ID: {prev_job_id}. Combination: ({fetch_job_from_db(prev_job_id).job_type}, {job_type}). Should create template")

# Below are experimental functions
def handle_soft_interrupt(signalNumber, frame):
    print(f"Terminated by signal {signalNumber}")
    print(frame)


signal.signal(signal.SIGTERM, handle_soft_interrupt)

