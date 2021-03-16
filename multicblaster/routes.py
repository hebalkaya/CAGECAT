"""Stores routes for Flask web application

Author: Matthias van den Belt
"""

# import statements
from flask import render_template, request, url_for, redirect, send_file
from multicblaster import app, q, r
import multicblaster.utils as ut
from multicblaster.models import Job
from multicblaster import db
import multicblaster.workers as rf
import os

# route definitions
@app.route("/rerun/<prev_run_id>")
@app.route("/")
def home_page(prev_run_id=None):
    return show_template("index.xhtml", submit_url=ut.SUBMIT_URL, prev_run_id=prev_run_id)

@app.route(ut.SUBMIT_URL, methods=["POST"])
def submit_job():
    job_type = request.form["job_type"]
    job_id = ut.generate_job_id()

    ut.create_directories(job_id)

    if job_type == "search":
        f = rf.cblaster_search

        # save the files
        input_type = request.form["inputType"]
        if input_type == 'fasta':
            file_path = ut.save_file(request.files["genomeFiles"], job_id)
        elif input_type == "ncbi_entries":
            file_path = None
        elif input_type == "prev_session":
            file_type = request.form["searchPreviousType"]
            job_type = "recompute"

            if file_type == "jobID":
                prev_job_id = request.form["searchEnteredJobId"]

                ut.check_valid_job(prev_job_id, job_type)

                file_path = os.path.join(ut.LOGGING_BASE_DIR, prev_job_id, "results", f"{prev_job_id}_session.json")

            elif file_type == "sessionFile":
                file_path = ut.save_file(request.files["searchUploadedSessionFile"], job_id)
            else:
                raise IOError("Not valid file type")
        else: # future input types and prev_session
            raise NotImplementedError()
    elif job_type == "gne":
        f = rf.cblaster_gne

        file_type = request.form["gnePreviousType"]

        if file_type == "jobID":
            prev_job_id = request.form["gneEnteredJobId"]

            ut.check_valid_job(prev_job_id, job_type)

            file_path = os.path.join(ut.LOGGING_BASE_DIR, prev_job_id, "results", f"{prev_job_id}_session.json")
        elif file_type == "sessionFile":
            file_path = ut.save_file(request.files["gneUploadedSessionFile"], job_id)
        else:
            raise IOError("Not valid file type")

    ut.save_settings(request.form, job_id)
    job = q.enqueue(f, args=(job_id,),kwargs={
        "options": request.form,
        "file_path": file_path,
        "prev_page": "/" + request.referrer.split("/")[-1]
    }, result_ttl=86400)

    j = Job(id=job_id, status="queued", job_type=job_type)
    db.session.add(j)
    db.session.commit()

    return redirect(url_for("show_result", job_id=job_id))

@app.route("/results/<job_id>")
def show_result(job_id):
    job = ut.fetch_job_from_db(job_id)

    if job is not None:
        settings = ut.load_settings(job_id)
        status = job.status

        if status == "finished":

            with open(os.path.join(ut.LOGGING_BASE_DIR, job_id, "results", f"{job_id}_plot.html")) as inf:
                plot_contents = inf.read()

            return show_template("result_page.xhtml", job_id=job_id, status=status, compr_formats=ut.COMPRESSION_FORMATS, plot_contents=plot_contents)
        elif status == "failed":
            with open(os.path.join(ut.LOGGING_BASE_DIR, job_id, "logs", f"{job_id}_cblaster.log")) as inf:
                log_contents = "<br/>".join(inf.readlines())

            return show_template("failed_job.xhtml", settings=settings, job_id=job_id, log_contents=log_contents)
        elif status == "queued" or status == "running":
            return show_template("status_page.xhtml", job_id=job_id, status=status, settings=settings)
        else:
            raise IOError(f"Incorrect status of job {job_id} in database")

    else: # indicates no such job exists in the database
        return show_template("job_not_found.xhtml", job_id=job_id)
        # return render_template("job_not_found.xhtml", job_id=job_id,
        #                        serv_info=ut.get_server_info(q, r))

        # TODO: create not_found template

@app.route("/download-results/<job_id>", methods=["POST"])
def return_user_download(job_id):
    print(request.form)

    # execute convert_compression.py
    submitted_data = request.form
    print(submitted_data)
    if len(submitted_data) != 2: # should be job_id and compression_type
        # flash("Invalid post attributes") # TODO: should show them on the page
        return redirect(url_for("home_page"))

    compr_type = submitted_data["compression_type"]

    # TODO: first, execute compression_conversion script
    # to go from ours server-default compression to the desired compresion
    # format

    # TODO: send_from_directory is a safer approach, but this suits for now
    # as Flask should not be serving files when deployed
    return send_file(os.path.join(app.config["DOWNLOAD_FOLDER"], job_id, "results", f"{job_id}.zip"))

@app.route("/extract-sequence")
def extract_sequence():
    # TODO
    return 404

@app.route("/results", methods=["GET", "POST"])
def result_from_jobid():
    if request.method == "GET":
        return show_template("result_from_jobid.xhtml")
        # return render_template("result_from_jobid.xhtml", serv_info=ut.get_server_info(q, r))
    else: # method is POST
        job_id = request.form["job_id"]
        if ut.fetch_job_from_db(job_id) is not None:
            return redirect(url_for('show_result', job_id=job_id))
        else:
            return show_template("job_not_found.xhtml", job_id=job_id)
            # return "No job known with that ID" #TODO: create invalid job ID template

# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    return show_template("page_not_found.xhtml", stat_code=404)


@app.errorhandler(405)
def invalid_method(error):
    return redirect(url_for("home_page"))


def show_template(template_name: str, stat_code=None, **kwargs):
    """Returns rendered templates to the client

    Input:
        - template_name: name of template to be rendered. By default,
            templates should be located in the templates/ folder
        - stat_code, int: HTTP status code to be returned to the client
        - kwargs: keyword arguments used during rendering of the template

    Output:
        - rendered template

    Function was created to prevent redundancy when getting the server info
    and uses Flask's render_template function to actually render the templates
    """
    if stat_code is None:
        return render_template(template_name, serv_info=ut.get_server_info(q, r), **kwargs)
    else:
        return render_template(template_name, serv_info=ut.get_server_info(q, r), **kwargs), stat_code
