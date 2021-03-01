from flask import Flask, render_template, request, url_for, redirect, \
    send_from_directory, flash
from utils import get_server_info, save_file, FILE_POST_FUNCTION_ID_TRANS, \
    fetch_base_error_message, COMPRESSION_FORMATS, generate_job_id, \
    create_directories, LOGGING_BASE_DIR
import workers as rf
import HTMLGenerators as htmlg
import os
import redis
import rq

# TODO: Find out how pre-submission uploading works
if __name__ == "__main__":
    r = redis.Redis()
    q = rq.Queue(connection=r, default_timeout=28800) # 8h for 1 job

    app = Flask("multicblaster")
    UPLOAD_FOLDER = os.path.join("static", "uploads")
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    #logging.basicConfig(filename="logs.log", level=logging.INFO)
    SUBMIT_URL = "/submit_job"

# Views

@app.route("/")
def home_page():
    # TODO: create function to fetch server info
    return render_template("index.xhtml", submit_url=SUBMIT_URL,
                           serv_info=get_server_info(q, r))


@app.route("/new_job", methods=["GET"])
def new_job():
    return render_template("new_job.xhtml", serv_info=get_server_info(q, r))


@app.route(SUBMIT_URL, methods=["POST"])
def submit_job():
    job_type = request.form["job_type"]

    if job_type == "search":
        f = rf.cblaster_search
    elif job_type == "gne":
        raise NotImplementedError()# in case


    # Here we add a dummy function to add to the queue
    job_id = generate_job_id() # TODO: check if job ID is already in database
    # prev_page =
    # print(prev_page)

    print(request.form)
    create_directories(job_id) # FLASK should be ran on linux
    print("Succesfully created directories")

    # save the files
    input_type = request.form["inputType"]
    if input_type == 'fasta':
        if request.files:
            for file_key in request.files :
                file = request.files[file_key]
                if file.filename != "": # indicates that no file was uploaded
                 # TODO: make filename safe
                    file_path = os.path.join(f"{LOGGING_BASE_DIR}", job_id,
                                             "uploads", file.filename)
                    file.save(file_path)
    elif input_type == "ncbi_entries":
        file_path = None
    else: # future input types and prev_session
        raise NotImplementedError()

    job = q.enqueue(f, args=(job_id,),kwargs={
        "options": request.form,
        "file_path": file_path, # TODO for uploaded files
        "prev_page": "/" + request.referrer.split("/")[-1]
    }, result_ttl=86400)


    # job = q.enqueue(rf.execute_dummy_cmd, job_id)
    # job = q.enqueue(rf.execute_cblaster, args=(job_id,), kwargs={
    #     "form": request.form,
    #     "files": request.files if request.files else None,
    #     "prev_page": "/" + request.referrer.split("/")[-1]
    # }, result_ttl=86400) # keep results for 1 day

    # TODO: dont pass full request object, it will crash
    # job = q.enqueue(rf.execute_dummy_cmd, job_id)
    return render_template("job_submitted.xhtml", job_id=job_id,
                           submitted_data=request.form,
                           serv_info=get_server_info(q, r))


    return redirect(url_for("home_page"), serv_info=get_server_info(q, r))


@app.route("/results/<job_id>")
def show_result(job_id):
    #TODO: search for job ID
    found = True

    # TODO: get status of the job
    status = "running"

    if found:
        return render_template("result_page.xhtml", job_id=job_id,
                               status=status, serv_info=get_server_info(q, r),
                               compr_formats=COMPRESSION_FORMATS)
        # TODO: create status template

    return render_template("not_found.xhtml", job_id=job_id,
                           serv_info=get_server_info(q))
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

    return render_template("create_database.xhtml", submit_url=SUBMIT_URL,
                           serv_info=get_server_info(q, r),
                           outf_name= htmlg.generate_output_filename_form(
                               "database_name"))


@app.route("/extract-sequence")
def extract_sequence():
    # TODO
    return 404

@app.route("/neighbourhood")
def calculate_neighbourhood():
    return render_template("neighbourhood.xhtml",
                           submit_url=SUBMIT_URL,
                           serv_info=get_server_info(q, r),
                           session_file_upload=htmlg.SESSION_FILE_UPLOAD,
                           outf_name=htmlg.generate_output_filename_form(
                               "output_name"))

# Error handlers
@app.errorhandler(404)
def invalid_method(error):
    #logging.error(utils.fetch_base_error_message(error, request))
    # return redirect(url_for("home_page"))
    return render_template("page_not_found.xhtml",
                           serv_info=get_server_info(q, r)), 404


@app.errorhandler(405)
def page_not_found(error):
    base = fetch_base_error_message(error, request)
    #logging.error(f"{base}, METHOD: {request.method}")
    return redirect(url_for("home_page"))




#print(app.config.keys())
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")