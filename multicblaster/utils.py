import os
import random
from rq.registry import StartedJobRegistry, FinishedJobRegistry
from multicblaster.models import Job, Statistic
from datetime import datetime
import re

LOGGING_BASE_DIR = os.path.join("multicblaster", "jobs")
FOLDERS_TO_CREATE = ["uploads", "results", "logs"]
SUBMIT_URL = "/submit_job"
SEP = os.sep
PATTERN = "\('(.+?)', '(.*?)'\)"
INVALID_JOB_COMBINATIONS = [("recompute", "recompute"), ("recompute", "gne")]

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
                      "sampling_space": "Sampling space"
                      }

FILE_POST_FUNCTION_ID_TRANS = {"create_database": "genomeFiles",
                               "calculate_neighbourhood": "outputFileName"
                               }

COMPRESSION_FORMATS = [".tar", ".tar.gz", ".gz", ".7z", ".zip", ".rar"]

TEST_PATH = ".."


class StatusException(Exception):
    def __init__(self, msg):
        super(StatusException, self).__init__(msg)


def generate_job_id(id_len=15):
    characters = []
    id = 0

    while id is not None:
        for i in range(id_len):
            if i % 4 == 0:
                min, max = 65, 90
            else:
                min, max = 48, 57

            characters.append(chr(random.randint(min, max)))

        job_id = "".join(characters)
        id = fetch_job_from_db(job_id)  # becomes None if no such job exists

    return job_id


def parse_error(error_msg):
    # print(error_msg)
    # print(type(error_msg))
    return str(error_msg).split()[0]


def fetch_base_error_message(error, request):
    return f"CODE:{parse_error(error)}, URL:{request.url}"


def format_status_message(status):  # TODO: can probably be removed
    msg = ["Job status:"]
    if status == "queued":
        pass
    elif status == "running":
        pass
    elif status == "finished":
        pass
    else:
        raise StatusException()

    return msg


def save_file(file_obj, job_id):
    # TODO: make filename safe
    file_path = os.path.join(f"{LOGGING_BASE_DIR}", job_id,
                             "uploads", file_obj.filename)
    file_obj.save(file_path)

    return file_path


# def save_file(posted_files, app):
#     for file in posted_files:
#         path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         if os.path.exists(path):
#             print("Overwriting...")
#             #raise FileExistsError("There already is a file at that path")
#         # We can return false here, indicating that something went wrong.
#         # The client side can then react by giving an error
#         # Maybe flashing messages?
#         file.save(path)
#         print(f"File: {file.filename} has been saved at {path}")

# def save_file(directory: str, posted_files: dict, app) -> None:
#     print(posted_files)
#     print(list(posted_files.keys()))
#     print(list(posted_files.values()))
#     print("-============================================")
#     # print(os.path.join(app.config['UPLOAD_FOLDER'], "temper"))
#     file = posted_files[POSTED_FILE_TRANSLATION[directory]]
#     print(file)
#     # print(file)
#     # print(filename)
#     file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#
#     print(f"File: {file.filename} has been saved at ")


def get_server_info(q, redis_conn) -> dict:
    # TODO: maybe we can instantiate this registry once instead of every time
    # we want some server info
    start_registry = StartedJobRegistry('default', connection=redis_conn)
    # above registry has the jobs in it which have been started, but are not
    # finished yet: running jobs.
    queued = len(q)
    running = len(start_registry)
    status = "idle" if queued == 0 and running == 0 else "active"

    data = {"server_status": status,
            "queued": queued,
            "running": running,
            "completed": Statistic.query.filter_by(
                name="finished").first().count}

    return data


def create_directories(job_id):
    base_path = f"{LOGGING_BASE_DIR}/{job_id}"
    os.mkdir(base_path)
    for folder in FOLDERS_TO_CREATE:
        os.mkdir(f"{base_path}/{folder}")
    # with open(f"{base_path}/logs/{job_id}.log", "w") as outf:
    #     # outf.write(f"{job_id}\n")
    #     cmd = ["pip3", "freeze"]
    #     subprocess.run(cmd, stderr=outf, stdout=outf, text=True)


def add_time_to_db(job_id, time_to_add, db):
    """

    :param job_id:
    :param time_to_add:
    :return:
    """
    job = fetch_job_from_db(job_id)
    print(job)
    if time_to_add == "start":
        job.start_time = datetime.utcnow()
    elif time_to_add == "finish":
        job.finish_time = datetime.utcnow()
    else:
        raise IOError("Invalid time type")

    db.session.commit()


def mutate_status(job_id, stage, db, return_code=None):
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


def load_settings(job_id):
    settings_dict = {}

    file_path = f"{LOGGING_BASE_DIR}{SEP}{job_id}{SEP}logs{SEP}{job_id}_options.txt"
    with open(file_path) as inf:
        settings = inf.read()

    matches = re.findall(PATTERN, settings[20:-2])
    for key, value in matches:
        label = PRETTY_TRANSLATION[key]

        if label is not None:
            settings_dict[label] = value

    return settings_dict


def save_settings(options, base_path):
    with open(f"{base_path}_options.txt", "w") as outf:
        outf.write(str(options))


def fetch_job_from_db(job_id: str) -> Job:
    """Checks if a job with a specific job ID exists in the database

    Input:
        - job_id: ID of a job to search for
    Output:
        - Job instance if present in the database OR
        - None if no job with the given ID was found in the database
    """
    return Job.query.filter_by(id=job_id).first()

def check_valid_job(prev_job_id: str, job_type: str):
    """Checks if a submitted job, relying on a previous job is valid

    :param prev_job_id: ID of the user-submitted previous job
    :param job_type: type of the submitted job e.g. "search" or "gne"

    Output: # TODO: might change into rendering templates
        - raises errors if the previous_job_id was not found in the database
            or the combinations of job types is invalid, which would cause
            multicblaster to crash
    """
    if fetch_job_from_db(prev_job_id) is None:
        # TODO: create invalid job ID template
        # TODO: OR let JS check job ID on front-end
        raise NotImplementedError("Invalid job ID. Template should be created")
    if (fetch_job_from_db(prev_job_id).job_type, job_type) in INVALID_JOB_COMBINATIONS:
        # TODO: should create template
        raise NotImplementedError(
            f"Invalid combinations of job types. Prev job ID: {prev_job_id}. Combination: ({fetch_job_from_db(prev_job_id).job_type}, {job_type}). Should create template")