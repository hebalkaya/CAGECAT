"""TODO: module docstring

"""

# package imports
from flask import Blueprint, request, redirect, url_for, send_file

# own project imports
from multicblaster import app
import multicblaster.utils as ut
import multicblaster.const as co
from multicblaster.routes_helpers import show_template
import multicblaster.routes_helpers as rthelp

# other imports
import os

# typing imports
import flask.wrappers
import typing as t

result = Blueprint('result', __name__, template_folder="templates")

### Route function definitions
@result.route("/<job_id>")
def show_result(job_id: str, pj=None, store_job_id=False, j_type=None) -> str: # parent_job should be
    """Shows the results page for the given job ID

    Input:
        - job_id: job ID for a previously submitted job for which the user
            would like to view the results

    Output:
        - HTML represented in string format. Renders different templates based
            on the status of the given job ID

    Raises:
        - IOError: when for some reason a job's status is not valid. Currently
            valid options are: ["finished", "failed", "queued", "running"]

    Shows the "job_not_found.xhtml" template when the given job ID was not
    found in the SQL database
    """
    job = ut.fetch_job_from_db(job_id)

    if job is not None:
        settings = ut.load_settings(job_id)
        status = job.status

        if status == "finished":
            module = job.job_type
            plot_contents, program, size = rthelp.prepare_finished_result(
                job_id, module)
            # plot contents is not used

            with open(os.path.join(ut.JOBS_DIR, job_id, "logs",
                                   f"{job_id}_{program}.log")) as inf:
                log_contents = "<br/>".join(inf.readlines())
            connected_jobs = rthelp.get_connected_jobs(job)

            return show_template("result_page.xhtml", j_id=job_id,
                                 status=status,
                                 content_size=ut.format_size(size),
                                 compr_formats=ut.COMPRESSION_FORMATS,
                                 module=module, modules_with_plots=
                                 ut.MODULES_WHICH_HAVE_PLOTS,
                                 # log_contents=log_contents,
                                 downstream_modules=
                                 co.DOWNSTREAM_MODULES_OPTIONS[module],
                                 connected_jobs=connected_jobs,
                                 help_enabled=False)

        elif status == "failed":
            with open(os.path.join(ut.JOBS_DIR, job_id,
                                   "logs", f"{job_id}_cblaster.log")) as inf:
                log_contents = "<br/>".join(inf.readlines())

            return show_template("failed_job.xhtml", settings=settings,
                                 j_id=job_id, log_contents=log_contents)

        elif status == "queued" or status == "running":

            if "pj" not in request.args:
                pj = "null"
            else:
                pj = request.args["pj"]

            return show_template("status_page.xhtml", j_id=job_id,
                                 parent_job=pj,
                                 status=status,
                                 settings=settings,
                                 store_job_id=store_job_id,
                                 j_title=ut.fetch_job_from_db(job_id).title,
                                 j_type=j_type,
                                 stat_code=302)

        elif status == "waiting":
            pj = ut.fetch_job_from_db(job_id).depending_on\
                if "pj" not in request.args else request.args["pj"]

            return show_template("status_page.xhtml", j_id=job_id,
                                 status="waiting for preceding job to finish",
                                 settings=settings,
                                 parent_job=pj,
                                 j_title=ut.fetch_job_from_db(job_id).title,
                                 store_job_id=store_job_id,
                                 j_type=j_type)
        else:
            raise IOError(f"Incorrect status of job {job_id} in database")

    else:  # indicates no such job exists in the database
        return show_template("job_not_found.xhtml", job_id=job_id)
        # TODO: create not_found template


@result.route("/download/<job_id>", methods=["GET", "POST"])
def return_user_download(job_id: str) -> flask.wrappers.Response:
    """Returns zipped file to client, enabling the user to download the file

    Input:
        - job_id: job ID for which the results are requested

    Output:
        - Downloads zipped file to the client's side. Therefore, the files
            stored on the server are transferred to the client

    Currently only supports downloading of the .zip file. No other
    compression formats are currently supported, even though the user has the
    ability to select a different compression format.
    """
    # execute convert_compression.py
    submitted_data = request.form

    # if len(submitted_data) != 2:  # should be job_id and compression_type
    #     return redirect(url_for("home_page"))
    if 'compression_type' in submitted_data:
        compr_type = submitted_data["compression_type"]

        # TODO: first, execute compression_conversion script
        # to go from ours server-default compression to the desired compresion
        # format

    # TODO: send_from_directory is a safer approach, but this suits for now
    # as Flask should not be serving files when deployed
    return send_file(os.path.join(app.config["DOWNLOAD_FOLDER"],
                                  job_id, "results", f"{job_id}.zip"))


@result.route("/", methods=["GET", "POST"])
def result_from_job_id() -> t.Union[str, str]: # actual other Union return type
    # is: werkzeug.wrappers.response.Response # TODO: fix this
    """Shows page for navigating to results page of job ID or that page itself

    Input:
        No inputs

    Output:
        - HTML represented in string format. Renders different templates
            whether the job ID is present in the SQL database or not ("POST"
            request), or the page for entered a job ID is requested ("GET"
            request).

    """
    if request.method == "GET":
        return show_template("result_from_jobid.xhtml", help_enabled=False)
    else:  # can only be POST as GET and POST are the only allowed methods
        job_id = request.form["job_id"]
        if ut.fetch_job_from_db(job_id) is not None:
            return show_template('redirect.xhtml', url=url_for('result.show_result', job_id=job_id))
        else:
            return show_template("job_not_found.xhtml", job_id=job_id)
            # TODO: create invalid job ID template


@result.route("/plots/<job_id>")
def get_plot_contents(job_id) -> str:
    """Returns the HTML code of a plot as a string

    Input:
        - job_id: job ID for which the plot is requested

    """
    return rthelp.prepare_finished_result(job_id, ut.fetch_job_from_db(
        job_id).job_type)[0]
