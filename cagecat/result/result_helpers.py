"""Helper functions involved in results

Author: Matthias van den Belt
"""

import os
import re
import typing as t

from flask import url_for

from cagecat.const import failure_reasons, jobs_dir, regex_failure_reasons
from cagecat.db_models import Job as dbJob
from cagecat.general_utils import fetch_job_from_db, send_email
from config_files.sensitive import sender_email


def get_failure_reason(job_id: str) -> str:
    """Gets the user-friendly failure reason when a job has failed

    Input:
        - job_id: job id which has failed and the reason should be looked
            up for

    Output:
        - user-friendly failure reason
    """
    msg = None
    try:
        with open(os.path.join(jobs_dir, job_id, "logs", f"{job_id}.log")) as inf:
            logs = inf.readlines()

        for l in logs:
            for fail in failure_reasons:
                if fail in l:
                    return failure_reasons[fail]

            for fail_pattern, message in regex_failure_reasons:
                if re.findall(pattern=fail_pattern, string=l):
                    return message

    except FileNotFoundError:
        msg = 'No log file was found for your analysis. The developers have been notified to investigate your scenario.'

    send_email(
        subject=f'{job_id} failed with an unknown reason.',
        message=f'The job {job_id} failed with an unknown reason. Link: {url_for("show_result", job_id=job_id)}',
        receiving_email=sender_email
    )

    if msg is None:
        return 'Unknown failure reason. The developers have been notified to investigate your scenario.'
    else:
        return msg


def prepare_finished_result(job_id: str,
                            module: str) -> \
        t.Tuple[t.Union[str, None], str, t.Union[int, None]]:
    """Returns HTML code of plots if applicable and appropriate program

    Input:
        - job_id: ID corresponding to the job the results are requested for
        - module: module type of given job id for which the results are
            requested

    Output:
        - plot_contents: HTML code of a plot
        - program: the program that was executed by this job
        - size: size of the returned plot in bytes
    """
    plot_path = os.path.join(jobs_dir, job_id,
                             "results", f"{job_id}_plot.html")
    size = None

    if module == "extract_sequences" or module == "extract_clusters":
        program = "cblaster"
        plot_contents = None

    elif module == "search" or module == "recompute" or module == "gne":
        program = "cblaster"
        with open(plot_path) as inf:
            plot_contents = inf.read()
        size = os.path.getsize(plot_path)

    elif module == "corason":
        program = "echo"  # TODO future: will be someting else later
        plot_contents = None  # TODO future: for now

    elif module == "clinker":
        program = "clinker"
        with open(plot_path) as inf:
            plot_contents = inf.read()
        size = os.path.getsize(plot_path)

    elif module == "clinker_query":
        program = "cblaster"  # as it uses plot_clusters functionality of cblaster
        with open(plot_path) as inf:
            plot_contents = inf.read()
        size = os.path.getsize(plot_path)
    else:
        raise NotImplementedError(
            f"Module {module} has not been implemented yet in results")

    return plot_contents, program, size


def get_connected_jobs(job: t.Optional[dbJob]) -> \
        t.List[t.Tuple[str, str, str, str, str], ]:
    """Gets the connected (children, main_search, depending) jobs of a job

    Input:
        - job entry in SQL db for which connected jobs are requested

    Output:
        - connected jobs. Format of connected job:
            [job_id, job_title, job_type, job_status, connection_type]

    Child jobs: jobs which use the output of preceding jobs as input
    Main search: job which was used to search (initial job)
    Depending: jobs on which the current job depends to start
    """
    connected_jobs = []

    if job.main_search_job == "null": # current job is an initial job (search of clinker)
        # go and look for child jobs
        children = job.child_jobs

        if children:  # empty string evaluates to False
            for j_id in children.split(","):
                child_job = fetch_job_from_db(j_id)
                connected_jobs.append((child_job.id, child_job.title, child_job.job_type, child_job.status, "child"))

    else:
        main_job = fetch_job_from_db(job.main_search_job)
        connected_jobs.append((main_job.id, main_job.title, main_job.job_type, main_job.status, "main search"))

        if job.depending_on != "null":
            parent_job = fetch_job_from_db(job.depending_on)
            connected_jobs.append((parent_job.id, parent_job.title, parent_job.job_type, parent_job.status, "depending"))

    return connected_jobs
