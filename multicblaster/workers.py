"""Stores (helper) functions to execute when a submitted job will be executed

Author: Matthias van den Belt
"""

# import statements
import subprocess
import os
from multicblaster.utils import JOBS_DIR, add_time_to_db, mutate_status
from multicblaster import db
import werkzeug.datastructures
import typing as t

# Whenever a CMD is ran from a function, all print statements within that
# same function are performed when the CMD has finished

# redis-queue functions
def first(job_id, options=None, file_path=None):
    print(f"This is the first function. JID: {job_id}")
    post_job_formalities(job_id, 0)

def second(job_id, options=None, file_path=None):
    print(f"Second function?!!!?! JID: {job_id}")
    post_job_formalities(job_id, 0)

def cblaster_search(job_id, options=None, file_path=None):
    pre_job_formalities(job_id)

    _, LOG_PATH, RESULTS_PATH = generate_paths(job_id)
    recompute = False

    # create the base command, with all required fields
    cmd = ["cblaster", "search",
           "--output", os.path.join(RESULTS_PATH, f"{job_id}_summary.txt"),
           "--plot", os.path.join(RESULTS_PATH, f"{job_id}_plot.html")]

    # add input options
    input_type = options["inputType"]

    if input_type == "fasta":
        cmd.extend(["--query_file", file_path])
        session_path = os.path.join(RESULTS_PATH, f"{job_id}_session.json")
    elif input_type == "ncbi_entries":
        cmd.append("--query_ids")
        cmd.extend(options["ncbiEntriesTextArea"].split())
        session_path = os.path.join(RESULTS_PATH, f"{job_id}_session.json")
    elif input_type == "prev_session":
        recompute = True
        cmd.extend(["--recompute",
                    os.path.join(RESULTS_PATH, f"{job_id}_recomputed.json")])
        session_path = file_path

    else:  # future input types and prev_session
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
    cmd.extend(["--binary",
                os.path.join(RESULTS_PATH, f"{job_id}_binary.txt")])

    bin_table_delim = options["searchBinTableDelim"]
    if bin_table_delim:
        cmd.extend(["--binary_delimiter", bin_table_delim])

    cmd.extend(["--binary_decimals", options["searchBinTableDecimals"]])

    if "searchBinTableHideHeaders" in options:
        cmd.append("--binary_hide_headers")

    cmd.extend(["--binary_key", options["keyFunction"]])

    # TODO: maybe it can also be used with len as keyfunction
    if "hitAttribute" in options:  # only when keyFunction is not len
        cmd.extend(["--binary_attr", options["hitAttribute"]])

    # add additional options
    if "sortClusters" in options:
        cmd.append("--sort_clusters")

    return_code = run_command(cmd, LOG_PATH, job_id)
    post_job_formalities(job_id, return_code)


def cblaster_gne(job_id, options=None, file_path=None):
    """

    :param job_id:
    :param options:
    :param file_path: session file path
    :return:
    """
    pre_job_formalities(job_id)

    _, log_path, results_path = generate_paths(job_id)

    session_path = file_path

    cmd = ["cblaster", "gne", session_path,
           "--max_gap", options["max_intergenic_distance"],
           "--samples", options["sample_number"],
           "--scale", options["sampling_space"],
           "--plot", os.path.join(results_path, f"{job_id}_plot.html"),
           "--output", os.path.join(results_path, f"{job_id}_summary.txt")]

    # TODO: test if gne also works with a job_id
    cmd.extend(create_summary_table_commands('gne', options))

    return_code = run_command(cmd, log_path, job_id)

    post_job_formalities(job_id, return_code)


def cblaster_extract_sequences(job_id, options=None, file_path=None):
    pre_job_formalities(job_id)
    _, LOG_PATH, RESULTS_PATH = generate_paths(job_id)

    extension = "txt"
    if "downloadSeqs" in options:
        extension = "fasta"

    cmd = ["cblaster", "extract", file_path,
           "--output", os.path.join(RESULTS_PATH, f"{job_id}_sequences.{extension}")]

    if options["selectedQueries"]:
        cmd.append("--queries")
        cmd.extend(options["selectedQueries"].split())

    # TODO: add organism filtering

    if options["selectedScaffolds"]:
        cmd.append("--scaffolds")
        cmd.extend(options["selectedScaffolds"].split())

    if "outputDelimiter" in options:
        cmd.extend(["--delimiter", options["outputDelimiter"]])

    if "nameOnly" in options:
        cmd.append("--name_only")

    if "downloadSeqs" in options:
        cmd.append("--extract_sequences")

    return_code = run_command(cmd, LOG_PATH, job_id)
    post_job_formalities(job_id, return_code)

def cblaster_extract_clusters(job_id, options=None, file_path=None):
    pre_job_formalities(job_id)
    _, LOG_PATH, RESULTS_PATH = generate_paths(job_id)

    # cluster_dir = os.path.join(RESULTS_PATH, "clusters")
    # os.mkdir(cluster_dir)

    cmd = ["cblaster", "extract_clusters", file_path,
           "--output", RESULTS_PATH]

    # TODO: add organism filtering

    if options["selectedScaffolds"]:
        cmd.append("--scaffolds")
        cmd.extend(options["selectedScaffolds"].split())

    if options["clusterNumbers"]:
        cmd.append("--clusters")
        cmd.extend(options["clusterNumbers"].strip().split())

    if options["clusterScoreThreshold"]:
        cmd.extend(["--score_threshold", options["clusterScoreThreshold"]])

    if options["prefix"]:
        cmd.extend(["--prefix", options["prefix"]])

    cmd.extend(["--format", options["format"]])
    cmd.extend(["--maximum_clusters", options["maxclusters"]])

    for a in cmd:
        print(a, type(a))
        # print(type(a))
    return_code = run_command(cmd, LOG_PATH, job_id)
    post_job_formalities(job_id, return_code)


# auxiliary functions
def create_summary_table_commands(
        module: str, options: werkzeug.datastructures.ImmutableMultiDict) \
        -> t.List[str]:
    """Generates commands for creating a summary table

    Input:
        - module: name of used multicblaster module to create commands for.
            Currently available are: ["search", "gne"]
        - options: user submitted options (values) via HTTP form of front-end

    Output:
        - summary_cmds: commands to enable creation of a custom-defined
            summary table

    Depending on the module, a prefix is required for the commands to work.
    """
    summary_cmds = []

    if module == "search":
        prefix = "output_"
    elif module == "gne":
        prefix = ""
    else:
        raise IOError("Invalid module")

    sum_table_delim = options[f"{module}SumTableDelim"]
    if sum_table_delim:  # evalutes to True if not an empty string
        summary_cmds.extend([f"--{prefix}delimiter", sum_table_delim])

    summary_cmds.extend([f"--{prefix}decimals",
                         options[f"{module}SumTableDecimals"]])

    if f"{module}SumTableHideHeaders" in options:
        summary_cmds.append(f"--{prefix}hide_headers")

    return summary_cmds


def run_command(cmd: t.List[str], log_base: str, job_id: str) -> int:
    """Executes a command on the command line

    Input:
        - cmd: split command to be executed. All elements in the
            list are joined together with a space to form a full command
        - log_base: base directory for logging. Has the following structure:
            "multicblaster/jobs/{job_id}/logs/"
        - job_id: ID corresponding to the job the function is called for

    Output:
        - res.returncode: exit code of the executed command. A non-zero exit
            code indicates something went wrong. An exit code of 0 indicates
            the command has executed without any problems.

    # TODO: add graceful termination handling by SIGTERM. When terminated
    # status should be changed to "failed" and "finish" time should be added
    """
    log_command(cmd, log_base, job_id)

    with open(os.path.join(log_base, f"{job_id}_{cmd[0]}.log"), "w") as outf:
        res = subprocess.run(cmd, stderr=outf, stdout=outf, text=True)

    return res.returncode


def generate_paths(job_id: str) -> t.Tuple[str, str, str]:
    """Returns paths for logging and result directories

    Input:
        - job_id: ID corresponding to the job the function is called for

    Output:
        - [0]: base path for the job
        - [1]: path for the logging directory
        - [2]: path for the results directory
    """
    base = os.path.join(JOBS_DIR, job_id)
    return base, os.path.join(base, "logs"), os.path.join(base, "results")


def zip_results(job_id: str) -> None:
    """Zips all files belonging to a job (logs, results, uploads)

    Input:
        - job_id: ID corresponding to the job the function is called for

    Output:
        - None
        - A .zip file containing all files which are part of a job

    We change directories to the {job_id} folder, which contains 3 folders:
    1. logs; 2. results; 3. uploads; Therefore, the paths used in this
    function are relative to the {job_id} folder.
    """
    base, log_dir, results_dir = generate_paths(job_id)
    os.chdir(base)  # go 1 level up

    cmd = ["zip", "-r", os.path.join("results", f"{job_id}.zip"), "."]
    # all files and folders in the current directory
    # (multicblaster/jobs/{job_id}/ under the base folder

    run_command(cmd, "logs", job_id)
    # invalid path: 'logs/U812J131P392S71_zip.txt/U812J131P392S71_cmd.txt'
    # something is going wrong


def log_command(cmd: t.List[str], log_base: str, job_id: str) -> None:
    """Logs the executed command to a file

    Input:
        - cmd: split command to be executed. All elements in the
            list are joined together with a space to form a full command
        - log_base: base directory for logging. Has the following structure:
            "multicblaster/jobs/{job_id}/logs/"
        - job_id: ID corresponding to the job the function is called for

    Output:
        - None
        - .txt file with the executed command
    """
    with open(os.path.join(log_base,
                           f"{job_id}_{cmd[0]}_cmd.txt"), "w") as outf:
        outf.write(" ".join(cmd))


def pre_job_formalities(job_id: str) -> None:
    """Wrapper function for functions to be executed pre-job execution

    Input:
        - job_id: ID corresponding to the job the function is called for

    Output:
        - None
        - See documentation of executed functions for their corresponding
            outputs
    """
    add_time_to_db(job_id, "start", db)
    mutate_status(job_id, "start", db)


def post_job_formalities(job_id: str, return_code: int) -> None:
    """Wrapper function for functions to be executed post-job execution

    Input:
        - job_id: ID corresponding to the job the function is called for
        - return_code: exit code of the executed command. A non-zero exit
            code indicates something went wrong. An exit code of 0 indicates
            the command has executed without any problems.

    Output:
        - None
        - See documentation of executed functions for their corresponding
            outputs
    """
    zip_results(job_id)
    add_time_to_db(job_id, "finish", db)
    mutate_status(job_id, "finish", db, return_code=return_code)


