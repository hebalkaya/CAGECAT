"""Stores helper functions of the routes.py module

Author: Matthias van den Belt
"""

# package imports
from flask import render_template, request
import os

# own project imports
import cagecat.utils as ut
from cagecat import q, r
from cagecat.models import Job as dbJob
from cagecat import db
from cagecat.classes import CAGECATJob

# typing imports
import typing as t
from werkzeug.datastructures import ImmutableMultiDict

### Function definitions
def get_connected_jobs(job: t.Optional[dbJob]) -> \
        t.List[t.Tuple[str, str, str, str], ]:
    """Gets the connected (children, main_search, depending) jobs of a job

    Input:
        - job entry in SQL db for which connected jobs are requested

    Output:
        - connected jobs. Format of connected job:
            [job_id, job_type, job_status, connection_type]

    Child jobs: jobs which use the output of preceding jobs as input
    Main search: job which was used to search (initial job)
    Depending: jobs on which the current job depends to start
    """
    connected_jobs = []

    if job.main_search_job == "null": # current job is a search job (or comes from session file?)
        # go and look for child jobs
        children = job.child_jobs

        if children:  # empty string evaluates to False
            for j_id in children.split(","):
                child_job = ut.fetch_job_from_db(j_id)
                connected_jobs.append((child_job.id, child_job.job_type, child_job.status, "child"))

    else:
        main_job = ut.fetch_job_from_db(job.main_search_job)
        connected_jobs.append((main_job.id, main_job.job_type, main_job.status, "main search"))

        if job.depending_on != "null":
            parent_job = ut.fetch_job_from_db(job.depending_on)
            connected_jobs.append((parent_job.id, parent_job.job_type, parent_job.status, "depending"))

    return connected_jobs


def show_template(template_name: str, help_enabled:bool = True,
                  stat_code=None, **kwargs) -> t.Union[str, t.Tuple[str, int]]:
    """Returns rendered templates to the client

    Input:
        - template_name: name of template to be rendered. By default,
            templates should be located in the templates/ folder
        - help_enabled: show help pane
        - stat_code, int: HTTP status code to be returned to the client
        - kwargs: keyword arguments used during rendering of the template

    Output:
        - rendered template (HTML code) represented in string format

    Function was created to prevent redundancy when getting the server info
    and uses Flask's render_template function to actually render the templates
    """
    if stat_code is None:
        return render_template(template_name, help_enabled=help_enabled,
                               serv_info=ut.get_server_info(q, r), **kwargs)
    else:
        return render_template(template_name, help_enabled=help_enabled,
                               serv_info=ut.get_server_info(q, r),
                               **kwargs), stat_code


def get_previous_job_properties(job_id: str, job_type: str,
                                module: str) -> str:
    """Returns appropriate file path of previous job

    Input:
        - job_id: ID corresponding to the job the properties are asked for
        - job_type: type of job (e.g. search, recomputation or extraction)
        - module: name of module for which the properties are asked for

    Output:
        - file_path: appropriate file path to be used in the next steps
    """
    file_type = request.form[f"{module}PreviousType"]
    if file_type == "jobID":
        prev_job_id = request.form[f"{module}EnteredJobId"]

        ut.check_valid_job(prev_job_id)

        file_path = os.path.join(ut.JOBS_DIR, prev_job_id, "results",
                                 f"{prev_job_id}_session.json")
    elif file_type == "sessionFile":
        file_path = ut.save_file(
            request.files[f"{module}UploadedSessionFile"], job_id)
    else:
        raise IOError("Not valid file type")

    return file_path


def prepare_search(job_id: str, job_type: str) -> t.Tuple[str, str]:
    """Parses input type for search module

    Input:
        - job_id: ID corresponding to the job the properties are asked for
        - job_type: type of job (e.g. search, recomputation or extraction)

    Output:
        - file_path: appropriate file path to be used in the next steps
        - job_type: type of job (e.g. search, recomputation or extraction)
            is changed when the the user asked for a recomputation
    """
    # save the files
    if 'inputType' in request.form:
        input_type = request.form["inputType"]

        if input_type == 'fasta':
            file_path = ut.save_file(request.files["genomeFiles"], job_id)
        elif input_type == "ncbi_entries":
            file_path = None
        elif input_type == "prev_session":
            job_type = "recompute"
            file_path = get_previous_job_properties(job_id, job_type, "search")
        else:
            raise NotImplementedError(
                f"Input type {input_type} has not been implemented yet")
    else:
        file_path, job_type = None, 'search'

    return file_path, job_type


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
    plot_path = os.path.join(ut.JOBS_DIR, job_id,
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
        program = "echo"  # TODO: must: will be someting else later
        plot_contents = None  # TODO: must: for now

    elif module == "clinker_full":
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


def enqueue_jobs(new_jobs: t.List[CAGECATJob]) -> str:
    # TODO: documentation
    """Enqueues jobs on the Redis queue

    Input:
        - new_jobs: list of tuples where each tuple represents an entire job,
            storing all required properties of a job within that tuple.
            Indexes:
                0 -> appropriate worker function
                1 -> job ID
                2 -> client form submitted by user
                3 -> file path: represents either path to a session file of
                     previous job or an output path
                4 -> job ID of the job where the current job depends on
                5 -> type of the job
                6 -> title of the job
                7 -> email of the job

    Output:
        - last_job_id: job ID of the last added job. Used to show appropriate
            results page and fetch a job which this job depends on, if
            applicable
    """
    if len(new_jobs) == 0:
        raise IOError("Submitted a job, but no job added to the list")

    created_redis_jobs_ids = []

    for i, cc_job in enumerate(new_jobs):  # cc_job = cagecat_job (CAGECATJob)
        ut.create_directories(cc_job.job_id)
        ut.save_settings(cc_job.options, cc_job.job_id)

        depending_on = None if cc_job.depending_on.job_id is None else \
            created_redis_jobs_ids[i-1][1]

        job = q.enqueue(cc_job.function,
                        args=(cc_job.job_id),
                        kwargs={'options': cc_job.options,
                                'file_path': cc_job.file_path},
                        depends_on=depending_on,
                        result_ttl=86400)

        main_search_job_id = add_parent_search_and_child_jobs_to_db(cc_job, i == len(new_jobs)-1)

        j = dbJob(id=cc_job.job_id,
                  status="queued" if depending_on is None else "waiting",  # for parent job to finish
                  job_type=cc_job.get_job_type(),
                  redis_id=job.job_id,
                  depending_on='null' if depending_on is None else cc_job.depending_on.job_id,
                  main_search_job=main_search_job_id,
                  title=cc_job.title,
                  email=cc_job.email)

        db.session.add(j)
        db.session.commit()

        created_redis_jobs_ids.append((cc_job.job_id, job.job_id))
        last_job_id = cc_job.job_id

    return last_job_id


def add_parent_search_and_child_jobs_to_db(new_job: CAGECATJob,
                                           is_last_job: bool) -> str:
    # TODO: change documentation
    """Adds the main search job and its children to the new_job in db

    Input:
        - new_job: a job to be added with its options. For index explanation: see the
            enqueue_jobs function
        - is_last_job: indicates if this is the last job being added to the
            queue (used in enqueue_jobs())

    Output:
        - job id of the main search job
    """
    if new_job.get_job_type() == 'search':
        main_search_job_id = "null"
    else:
        old_job = get_parent_job(new_job, is_last_job)

        if old_job.job_type == "search":
            main_search_job = ut.fetch_job_from_db(old_job.id)

            sep = "" if not main_search_job.child_jobs else ","
            main_search_job.child_jobs += f"{sep}{new_job.job_id}"
            # empty string for the first child job
        else:
            main_search_job_id = old_job.main_search_job

    return main_search_job_id


def get_parent_job(new_job: CAGECATJob,
                                 is_last_job: bool) -> t.Union[None, dbJob]:
    # TODO: change documentation
    """Gets the parent job of a job (i.e. the job this job depends on)

    Input:
        - new_job: a job to be added with its options. For index explanation: see the
            enqueue_jobs function
        - is_last_job: indicates if this is the last job being added to the
            queue (used in enqueue_jobs())

    Output:
        - parent Job instance
    """
    j_type = new_job.get_job_type()
    if j_type in ("recompute", "gne", "clinker_full"):
        # are modules which use the prev_session macro to get the previous session ID
        # might change in the future

        # below lines are required due to the naming in the HTML input fields
        if j_type == "recompute":
            module = "search"
        elif j_type == "clinker_full":
            module = "clinker"
        else:
            module = j_type

        key = f"{module}EnteredJobId"
    else:
        key = "prev_job_id"

    return ut.fetch_job_from_db(
        new_job.options[key] if is_last_job else new_job.file_path.split(os.sep)[2])
