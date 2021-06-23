# package imports
import subprocess
import os
import ssl
import smtplib

# own project imports
from multicblaster.utils import JOBS_DIR, add_time_to_db, mutate_status, \
    fetch_job_from_db, send_email
from multicblaster import db
from config import EMAIL, CONF

# typing imports
import werkzeug.datastructures
import typing as t

def create_filtering_command(options, is_cluster_related):
    partly_cmd = []

    if not is_cluster_related:
        if options["selectedQueries"]:
            partly_cmd.append("--queries")
            partly_cmd.extend(options["selectedQueries"].split())

    if options["selectedOrganisms"]:
        partly_cmd.extend(["--organisms", options['selectedOrganisms']])
        # TODO: could also that user gives multiple patterns. separated by ?

    # if options["selectedScaffolds"]:
    #     partly_cmd.append("--scaffolds")
    #     partly_cmd.extend(options["selectedScaffolds"].split())

    if is_cluster_related:
        if options["clusterNumbers"]:
            partly_cmd.append("--clusters")
            partly_cmd.extend(options["clusterNumbers"].strip().split())

        if options["clusterScoreThreshold"]:
            partly_cmd.extend(["--score_threshold",
                               options["clusterScoreThreshold"]])

        partly_cmd.extend(["--maximum_clusters", options["maxclusters"]])

    return partly_cmd


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


def send_notification_email(job):
    send_email(f'Your job: {job.title}' if job.title else f'Your job with ID {job.id} has finished',
               f'''Dear researcher,
    
The job (type: {job.job_type}) you submitted on {job.post_time} has finished running on {job.finish_time}).

You are able to perform additional downstream analysis by navigating to the results page of your job by going to:\n{CONF['DOMAIN']}results/{job.id}\n
Also, downloading your results is available on this web page.''',
               job.email)


    # TODO: possibly change sender_email and create a better message



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

    j =  fetch_job_from_db(job_id)
    if j.email:
        send_notification_email(j)


def store_query_sequences_headers(log_path, input_type, data):
    if input_type == "ncbi_entries":  # ncbi_entries
        headers = data
    elif input_type == "fasta":
        with open(data) as inf:
            headers = [line.strip()[1:] for line in
                       inf.readlines() if line.startswith(">")]

    with open(os.path.join(log_path, "query_headers.csv"), "w") as outf:
        outf.write(",".join(headers))
