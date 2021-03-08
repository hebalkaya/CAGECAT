from flask import render_template, request, url_for, redirect
from multicblaster import app, q, r
import multicblaster.utils as ut
from multicblaster.models import Job
from multicblaster import db
import multicblaster.workers as rf
import os

@app.route("/")
def home_page():
    # TODO: create function to fetch server info
    return render_template("index.xhtml", submit_url=ut.SUBMIT_URL,
                           serv_info=ut.get_server_info(q, r))


@app.route("/new_job", methods=["GET"])
def new_job():
    return render_template("new_job.xhtml", serv_info=ut.get_server_info(q, r))


@app.route(ut.SUBMIT_URL, methods=["POST"])
def submit_job():
    job_id = ut.generate_job_id()

    j = Job(id=job_id, status="queued")
    db.session.add(j)
    db.session.commit()

    print(request.form)
    ut.create_directories(job_id)

    job_type = request.form["job_type"]

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

            if file_type == "jobID":
                prev_job_id = request.form["searchEnteredJobId"]
                file_path = os.path.join(ut.LOGGING_BASE_DIR, prev_job_id, "results", f"{prev_job_id}_session.json")
                print(file_path)
            elif file_type == "sessionFile":
                file_path = ut.save_file(request.files["searchUploadedSessionFile"], job_id)
                # print(file_path)
            else:
                raise IOError("Not valid file type")
        else: # future input types and prev_session
            raise NotImplementedError()
    elif job_type == "gne":
        f = rf.cblaster_gne

        file_type = request.form["gnePreviousType"]

        if file_type == "jobID":
            prev_job_id = request.form["gneEnteredJobId"]
            file_path = os.path.join(ut.LOGGING_BASE_DIR, prev_job_id, "results", f"{prev_job_id}_session.json")
        elif file_type == "sessionFile":
            file_path = ut.save_file(request.files["gneUploadedSessionFile"], job_id)
            # print(file_path)
        else:
            raise IOError("Not valid file type")

    ut.save_settings(request.form, os.path.join(ut.LOGGING_BASE_DIR, job_id, "logs", job_id))
    job = q.enqueue(f, args=(job_id,),kwargs={
        "options": request.form,
        "file_path": file_path, # TODO for uploaded files
        "prev_page": "/" + request.referrer.split("/")[-1]
    }, result_ttl=86400)

    return redirect(url_for("show_result", job_id=job_id))

    return render_template("job_submitted.xhtml", job_id=job_id,
                           submitted_data=request.form,
                           serv_info=ut.get_server_info(q, r))


@app.route("/results/<job_id>")
def show_result(job_id):
    #TODO: search for job ID
    job = Job.query.filter_by(id=job_id).first()


    if job is not None:
        settings = ut.load_settings(job_id)
        status = job.status

        if status == "finished" or status == "failed":
            return render_template("result_page.xhtml", job_id=job_id, serv_info=ut.get_server_info(q, r),
                                   compr_formats=ut.COMPRESSION_FORMATS, status=status)
            # show results page
        elif status == "queued" or status == "running":
            return render_template("status_page.xhtml", job_id=job_id, serv_info=ut.get_server_info(q, r),
                                   status=status, settings=settings)
        else:
            raise IOError(f"Incorrect status of job {job_id} in database")

    else: # indicates no such job exists in the database
        return render_template("not_found.xhtml", job_id=job_id,
                               serv_info=ut.get_server_info(q, r))

    # TODO: get status of the job
    status = "running"

    # if found:
    #     return render_template("result_page.xhtml", job_id=job_id,
    #                            status=status, serv_info=ut.get_server_info(q, r),
    #                            compr_formats=ut.COMPRESSION_FORMATS)
        # TODO: create status template


    # TODO: create not_found template

@app.route("/download-results", methods=["POST"])
def return_user_download():
    print(request.form)

    # execute convert_compression.py
    submitted_data = request.form
    print(submitted_data)
    if len(submitted_data) != 2: # should be job_id and compression_type
        # flash("Invalid post attributes") # TODO: should show them on the page
        return redirect(url_for("home_page"))

    job_id = submitted_data["job_id"]
    compr_type = submitted_data["compression_type"]

    # TODO: first, execute compression_conversion script
    # to go from ours server-default compression to the desired compresion
    # format

    # print("-"*50)
    # print(job_id, compr_type)
    return "Example" # TODO: use send_from_directory to return file

    # return "Hello there"


@app.route("/create-database")
def create_database():
    # submitted_data

    return render_template("create_database.xhtml", submit_url=ut.SUBMIT_URL,
                           serv_info=ut.get_server_info(q, r),
                           outf_name=ut.htmlg.generate_output_filename_form(
                               "database_name"))


@app.route("/extract-sequence")
def extract_sequence():
    # TODO
    return 404

@app.route("/neighbourhood")
def calculate_neighbourhood():
    return render_template("neighbourhood.xhtml",
                           submit_url=ut.SUBMIT_URL,
                           serv_info=ut.get_server_info(q, r),
                           session_file_upload=ut.htmlg.SESSION_FILE_UPLOAD,
                           outf_name=ut.htmlg.generate_output_filename_form(
                               "output_name"))

# Error handlers
@app.errorhandler(404)
def invalid_method(error):
    #logging.error(utils.fetch_base_error_message(error, request))
    # return redirect(url_for("home_page"))
    return render_template("page_not_found.xhtml",
                           serv_info=ut.get_server_info(q, r)), 404


@app.errorhandler(405)
def page_not_found(error):
    base = ut.fetch_base_error_message(error, request)
    #logging.error(f"{base}, METHOD: {request.method}")
    return redirect(url_for("home_page"))

