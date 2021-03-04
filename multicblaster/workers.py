from time import sleep
from random import randint
import subprocess
import os
from multicblaster.utils import LOGGING_BASE_DIR, add_time_to_db
from multicblaster import db


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


def create_summary_table_commands(module, options):
    summary_cmds = []

    if module == "search":
        prefix = "output_"
    elif module == "gne":
        prefix = ""
    else:
        raise IOError("Invalid module")

    sum_table_delim = options[f"{module}SumTableDelim"]
    if sum_table_delim: # evalutes to True if not an empty string
        summary_cmds.extend([f"--{prefix}delimiter", sum_table_delim])

    summary_cmds.extend([f"--{prefix}decimals", options[f"{module}SumTableDecimals"]])

    if f"{module}SumTableHideHeaders" in options:
        summary_cmds.append(f"--{prefix}hide_headers")

    return summary_cmds


def cblaster_search(job_id, options=None, file_path=None, prev_page=None):
    pre_job_formalities(job_id)

    BASE_PATH = f"{LOGGING_BASE_DIR}{sep}{job_id}"
    RESULTS_PATH = f"{BASE_PATH}{sep}results{sep}"
    LOG_PATH = f"{BASE_PATH}{sep}logs{sep}"
    recompute = False

    #base_path = create_directories(job_id) # should probably be done when
    # getting the request to store the uploaded files

    # cmd = ["cblaster", "search", "-qf", "A0A411L027.1.fasta", "-o",
    #        f"{base_path}/results/{job_id}_cblaster.json"]

    # TODO: change -qf to uploaded file
    # create the basic command, with all required fields
    cmd = ["cblaster", "search",
           "--output", f"{RESULTS_PATH}{job_id}_summary.txt",
           # TODO: or add creating plot to standard options
           ]

    # add input options
    input_type = options["inputType"]

    if input_type == "fasta":
        cmd.extend(["--query_file", file_path])
        session_path = f"{RESULTS_PATH}{job_id}_session.json"
    elif input_type == "ncbi_entries":
        cmd.append("--query_ids")
        cmd.extend(options["ncbiEntriesTextArea"].split())
        session_path = f"{RESULTS_PATH}{job_id}_session.json"
    elif input_type == "prev_session":
        recompute = True
        # TODO: maybe the if's below are not required as the file path is given
        cmd.extend(["--recompute", f"{RESULTS_PATH}{job_id}_recomputed.json"])
        session_path = file_path
        # - Results in error when trying to recompute a recomputed session file -
    # ------------------------------------------------------------------------
#         Traceback (most recent call last):
#     File "/home/pi/Desktop/linux/bin/cblaster", line 8, in <module>
#     sys.exit(main())
#       File "/home/pi/Desktop/linux/lib/python3.7/site-packages/cblaster/main.py", line 441, in main
# testing=args.testing,
# File "/home/pi/Desktop/linux/lib/python3.7/site-packages/cblaster/main.py", line 201, in cblaster
# query_profiles=query_profiles,
# File "/home/pi/Desktop/linux/lib/python3.7/site-packages/cblaster/helpers.py", line 149, in get_sequences
# raise ValueError("Expected 'query_file' or 'query_ids', or 'query_profiles'")
# ValueError: Expected 'query_file' or 'query_ids', or 'query_profiles'

    # ------------------------------------------------------------------------


    else: # future input types and prev_session
        raise NotImplementedError()

    cmd.extend(["--session_file", session_path])

    # add search options
    if not recompute:
        cmd.extend([
            "--database", options["database_type"],
            "--entrez_query", options["entrez_query"],
            "--hitlist_size", options["max_hits"]])

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
    cmd.extend(create_summary_table_commands('search', options))

    # add binary table
    cmd.extend(["--binary", f"{RESULTS_PATH}{job_id}_binary.txt"]) # create a binary table

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
        cmd.extend(["--plot", f"{RESULTS_PATH}{job_id}_plot.html"])

    program = cmd[0]

    # with open(f"{logs_path}huh.txt", "w") as outf:
    #     print(cmd, file=outf)
    #     print("\n", file=outf)
    #     print(options, file=outf)
    #     print("\n", file=outf)
    #     print(" ".join(cmd), file=outf)

    log_settings(cmd, options, f"{LOG_PATH}{job_id}_cmd.txt")
    run_command(cmd, f"{LOG_PATH}{job_id}_{program}.log")

def run_command(cmd, log_path):
    with open(log_path, "w") as outf:
        subprocess.run(cmd, stderr=outf, stdout=outf, text=True)

def log_settings(cmd, options, settings_log_path):
    with open(settings_log_path, "w") as outf:
        outf.write(f"Sent options:\n{options}\n\nCommand:\n{' '.join(cmd)}\n")


def cblaster_gne(job_id, options=None, file_path=None, prev_page=None):
    """

    :param job_id:
    :param options:
    :param file_path: session file path
    :param prev_page:
    :return:
    """
    BASE_PATH = f"{LOGGING_BASE_DIR}{sep}{job_id}"
    RESULTS_PATH = f"{BASE_PATH}{sep}results{sep}"
    LOG_PATH = f"{BASE_PATH}{sep}logs{sep}"

    session_path = file_path

    cmd = ["cblaster", "gne", session_path,
           "--max_gap", options["max_intergenic_distance"],
           "--samples", options["sample_number"],
           "--scale", options["sampling_space"],
           "--plot", f"{RESULTS_PATH}{job_id}_plot.html"
           ]

    # TODO: test if gne also works with a job_id
    cmd.extend(create_summary_table_commands('gne', options))
    program = cmd[0]

    log_settings(cmd, options, f"{LOG_PATH}{job_id}_cmd.txt")
    run_command(cmd, f"{LOG_PATH}{job_id}_{program}.log")

def pre_job_formalities(job_id):
    add_time_to_db(job_id, "start", db)

def post_job_formalities(job_id):
    add_time_to_db(job_id, "finish", db)
