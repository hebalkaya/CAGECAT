from time import sleep
from random import randint
import subprocess
import os
from flask import url_for
from utils import LOGGING_BASE_DIR


sep = os.sep

# Whenever a CMD is ran from a function, all print statements within that
# same function are performed when the CMD has finished


# Redis functions
def dummy_sleeping(msg):
    to_sleep = randint(2, 6)
    with open(f"id1.txt", "w") as outf:
        outf.write(f"We are going to sleep for {to_sleep} seconds")
        outf.write("Zzzzz...")
        print("Is this also shown?")

    sleep(to_sleep)
    print(f"Wakey wakey! - Job finished. Msg: ({msg})")

# def create_directories(job_id):
#     base_path = f"{LOGGING_BASE_DIR}/{job_id}"
#     os.mkdir(base_path)
#     for folder in FOLDERS_TO_CREATE:
#         os.mkdir(f"{base_path}/{folder}")
#     # with open(f"{base_path}/logs/{job_id}.log", "w") as outf:
#     #     # outf.write(f"{job_id}\n")
#     #     cmd = ["pip3", "freeze"]
#     #     subprocess.run(cmd, stderr=outf, stdout=outf, text=True)
#
#     return base_path


def cblaster_search(job_id, options=None, file_path=None, prev_page=None):
    base_path = f"{LOGGING_BASE_DIR}{sep}{job_id}"
    results_path = f"{base_path}{sep}results{sep}"
    logs_path = f"{base_path}{sep}logs{sep}"

    #base_path = create_directories(job_id) # should probably be done when
    # getting the request to store the uploaded files

    # cmd = ["cblaster", "search", "-qf", "A0A411L027.1.fasta", "-o",
    #        f"{base_path}/results/{job_id}_cblaster.json"]

    # TODO: change -qf to uploaded file
    # create the basic command, with all required fields
    cmd = ["cblaster", "search",
           "--query_file", file_path,
           "--output", f"{results_path}{job_id}_summary.txt",
           "--session_file", f"{results_path}{job_id}_session.json"
           # TODO: or add creating plot to standard options
           # "--database", options["database_type"],
           # "--entrez_query", options["entrez_query"],
           # "--hitlist_size", options["max_hits"]
           ]


    # TODO: add search options
    # add filtering options
    cmd.extend(["--max_evalue", options["max_evalue"],
                "--min_identity", options["min_identity"],
                "--min_coverage", options["min_query_coverage"]])

    # add clustering options
    cmd.extend(["--gap", options["max_intergenic_gap"],
                "--unique", options["min_unique_query_hits"],
                "--min_hits", options["min_hits_in_clusters"]])

    if "requiredSequences" in options:
        cmd.append("--require")
        cmd.extend(options["requiredSequences"].split())

    # add summary table
    sum_table_delim = options["searchSumTableDelim"]
    if sum_table_delim: # evalutes to True if not an empty string
        cmd.extend(["--output_delimiter", sum_table_delim])

    cmd.extend(["--output_decimals", options["searchSumTableDecimals"]])

    if "searchSumTableHideHeaders" in options:
        cmd.append("--output_hide_headers")

    # add binary table
    cmd.extend(["--binary", f"{results_path}{job_id}_binary.txt"]) # create a binary table

    bin_table_delim = options["searchBinTableDelim"]
    if bin_table_delim:
        cmd.extend(["--binary_delimiter", bin_table_delim])

    cmd.extend(["--binary_decimals", options["searchBinTableDecimals"]])

    if "searchBinTableHideHeaders" in options:
        cmd.append("--binary_hide_headers")

    cmd.extend(["--binary_key", options["keyFunction"]])

    # TODO: maybe it can also be used with len as keyfunction
    if "hitAttribute" in options: # only when keyFunction is not len
        cmd.extend(["--binary_attr", options["hitAttribute"]])

    # add additional options
    if "sortClusters" in options:
        cmd.append("--sort_clusters")

    if "generatePlot" in options:
        cmd.extend(["--plot", f"{results_path}{job_id}_plot.html"])

    program = cmd[0]

    with open(f"{logs_path}{job_id}_cmd.txt", "w") as outf:
        outf.write(f"Sent options:\n{options}\n\nCommand:\n{' '.join(cmd)}\n")

    with open(f"{logs_path}{job_id}_{program}.log", "w") as outf:
        subprocess.run(cmd, stderr=outf, stdout=outf, text=True)

    print("We are finished :)")