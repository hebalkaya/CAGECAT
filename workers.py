from time import sleep
from random import randint
import subprocess
import os
from flask import url_for
LOGGING_BASE_DIR = "jobs"
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

def create_directories(job_id):
    base_path = f"{LOGGING_BASE_DIR}/{job_id}"
    os.mkdir(base_path)
    for folder in FOLDERS_TO_CREATE:
        os.mkdir(f"{base_path}/{folder}")
    # with open(f"{base_path}/logs/{job_id}.log", "w") as outf:
    #     # outf.write(f"{job_id}\n")
    #     cmd = ["pip3", "freeze"]
    #     subprocess.run(cmd, stderr=outf, stdout=outf, text=True)

    return base_path


def execute_cblaster(job_id, form=None, files=None, prev_page=None):
    sleep(randint(5, 12))
    # Using None for every keyword parameter allows future calls to this
    # function to exclude setting this keyword parameter when it is not
    # required
    base_path = create_directories(job_id)# TODO: uncomment for on linux

    # if files is not None or not files:
    #     for name, file in files.items():
    #         safe_filename = file.filename #TODO: make it a safe filename
    #         path = f"{base_path}/uploads/{safe_filename}"
    #         file.save(path)
    #         print(f"File saved: {path}")

    # Prints are not shown unless the cmd is not executed, or after the cmd
    # has finished
    print(form)
    print(files)
    print(job_id)
    # We can't do anything with the files because they are still part of the
    # request. They are not yet saved on the server. Possible solution: save
    # them from during request processing, and store links to the paths of
    # the files in the file keyword to use it here
    print(prev_page)

    print("Going to execute cblaster now")
    cmd = ["cblaster", "search", "-qf", "A0A411L027.1.fasta", "-o",
           f"{base_path}/results/{job_id}_cblaster.json"] # -o should point
    # to result directory
    program = cmd[0] # for pipeline stage

    with open(f"{base_path}/logs/{job_id}_{program}.log", "w") as outf: # should
        # point
        # to
        # log directory
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
