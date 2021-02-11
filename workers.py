from time import sleep
from random import randint
import subprocess
import os
from flask import url_for

LOGGING_BASE_DIR = "jobs" # on Unix, so /
FOLDERS_TO_CREATE = ["uploads", "results", "logs"]

# Redis functions
def dummy_sleeping(msg):
    to_sleep = randint(2, 6)
    with open(f"id1.txt", "w") as outf:
        outf.write(f"We are going to sleep for {to_sleep} seconds")
        outf.write("Zzzzz...")
        print("Is this also shown?")

    sleep(to_sleep)
    print(f"Wakey wakey! - Job finished. Msg: ({msg})")

def execute_cblaster(job_id, test):
    create_directories(job_id)




def create_directories(job_id):
    base_path = f"{LOGGING_BASE_DIR}/{job_id}"
    os.mkdir(base_path)
    for folder in FOLDERS_TO_CREATE:
        os.mkdir(f"{base_path}/{folder}")
    with open(f"{base_path}/logs/{job_id}.log", "w") as outf:
        # outf.write(f"{job_id}\n")
        cmd = ["pip3", "freeze"]
        subprocess.run(cmd, stderr=outf, stdout=outf, text=True)


# def execute_cblaster_cmd(req, job_id):
#     # create_directories() TODO: create directories for this job
#     print(req)
#     print(job_id)
#     # with open(f"./{job_id}_log.txt", "w") as logfile:
#     #     print("We are here", file=logfile)
#     previous_url = "/" + req.referrer.split("/")[-1]
#     print(previous_url)
#     sleep(5)
#
#         # if previous_url == url_for("create_database"):
#         #     print("ok")
#             # save_file("custom_databases", request.files.getlist(), app)
#             # save_file(request.files.getlist(FILE_POST_FUNCTION_ID_TRANS[
#             #                                     "create_database"]), app)
#             # TODO: here we can do something
#
#
#         # elif previous_url == url_for("calculate_neighbourhood"):
#         # save_file(request.files.getlist(FILE_POST_FUNCTION_ID_TRANS[
#         #                                 "calculate_neighbourhood"]), app)
#
#         # cmd = ["pip", "freeze"]
#         #
#         # subprocess.run(cmd, text=True, encoding="UTF-8")
#         # cmd = ['cblaster', 'search', '-qf', '1yjy.fa', '-s', 'test_run2.json']
#         #
#         # with open(r"C:\Users\matth\OneDrive\Opleidingen\Master_WUR\__Thesis"
#         #           r"\thesis_repo\outfile1.txt", "w") as outf:
#         #
#         #
#         #     subprocess.run(cmd, stdout=outf, stderr=outf,
        #                    text=True, encoding="UTF-8")
