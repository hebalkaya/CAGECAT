import os
import random
from rq.registry import StartedJobRegistry, FinishedJobRegistry

FILE_POST_FUNCTION_ID_TRANS = {"create_database": "genomeFiles",
                           "calculate_neighbourhood": "outputFileName"
                               }

COMPRESSION_FORMATS = [".tar", ".tar.gz", ".gz",  ".7z", ".zip", ".rar"]

TEST_PATH = "."

class StatusException(Exception):
    def __init__(self, msg):
        super(StatusException, self).__init__(msg)

def generate_job_id(id_len=15):
    job_id = []

    for i in range(id_len):
        if i % 4 == 0:
            min, max = 65, 90
        else:
            min, max = 48, 57

        job_id.append(chr(random.randint(min, max)))

    return "".join(job_id)


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

def save_file(posted_files, app):
    for file in posted_files:
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        if os.path.exists(path):
            print("Overwriting...")
            #raise FileExistsError("There already is a file at that path")
        # We can return false here, indicating that something went wrong.
        # The client side can then react by giving an error
        # Maybe flashing messages?
        file.save(path)
        print(f"File: {file.filename} has been saved at {path}")

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

