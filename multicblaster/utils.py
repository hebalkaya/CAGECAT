import os
import random
from rq.registry import StartedJobRegistry, FinishedJobRegistry
from multicblaster.models import Job
from datetime import datetime

LOGGING_BASE_DIR = "jobs"
FOLDERS_TO_CREATE = ["uploads", "results", "logs"]
SUBMIT_URL = "/submit_job"

FILE_POST_FUNCTION_ID_TRANS = {"create_database": "genomeFiles",
                           "calculate_neighbourhood": "outputFileName"
                               }

COMPRESSION_FORMATS = [".tar", ".tar.gz", ".gz",  ".7z", ".zip", ".rar"]

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
        id = Job.query.filter_by(id=job_id).first() # becomes None if no such job exists

    return job_id


def parse_error(error_msg):
    # print(error_msg)
    # print(type(error_msg))
    return str(error_msg).split()[0]

def fetch_base_error_message(error, request):
    return f"CODE:{parse_error(error)}, URL:{request.url}"


def format_status_message(status): #TODO: can probably be removed
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
    start_registry = StartedJobRegistry('default', connection=redis_conn)
    finished_registry = FinishedJobRegistry('default', connection=redis_conn)
    # above registry has the jobs in it which have been started, but are not
    # finished yet: running jobs.

    data = {"server_status": "running",
            "queued": len(q),
            "running": len(start_registry),
            "completed": len(finished_registry)}

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
    job = Job.query.filter_by(id=job_id).first()
    print(job)
    if time_to_add == "start":
        job.start_time = datetime.utcnow()
    elif time_to_add == "finish":
        job.finish_time = datetime.utcnow()
    else:
        raise IOError("Invalid time type")

    db.session.commit()


def mutate_status(job_id, stage, db, return_code=None):
    job = Job.query.filter_by(id=job_id).first()

    if stage == "start":
        new_status = "running"
    elif stage == "finish":
        if return_code is None:
            raise IOError("Return code should be provided")
        new_status = "finished" if not return_code else "failed"
    else:
        raise IOError("Invalid stage")

    job.status = new_status

    db.session.commit()

