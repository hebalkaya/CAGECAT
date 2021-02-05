from flask import Flask, render_template, request, url_for, redirect
from utils import get_server_info, save_file, POSTED_FILE_TRANSLATION, \
    fetch_base_error_message
import workers as rf
import HTMLGenerators as htmlg
import os
import redis
import rq

# TODO: Find out how pre-submission uploading works
if __name__ == "__main__":
    r = redis.Redis()
    q = rq.Queue(connection=r)

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
                           serv_info=get_server_info(q))


@app.route("/new_job", methods=["GET"])
def new_job():
    return render_template("new_job.xhtml", serv_info=get_server_info(q))


@app.route(SUBMIT_URL, methods=["POST"])
def submit_job():
    print(request.form)
    print(request.files)
    if request.method == "POST":

        previous_url = "/" + request.referrer.split("/")[-1]
        # url_for returns with leading /
        #
        # print(request.files)
        # print(request.referrer)
        # print(previous_url)
        # print(request.form)
        # print(url_for("create_database"))
        # TODO: lines below can be optimized
        if previous_url == url_for("create_database"):
            print("ok")
            # save_file("custom_databases", request.files.getlist(), app)
            save_file(request.files.getlist(POSTED_FILE_TRANSLATION[
                                                "create_database"]), app)
            # TODO: here we can do something


        elif previous_url == url_for("calculate_neighbourhood"):
            save_file(request.files.getlist(POSTED_FILE_TRANSLATION[
                                                "calculate_neighbourhood"]), app)

        # Here we add a dummy function to add to the queue
        job = q.enqueue(rf.dummy_sleeping, "this is a dummy function")
        print(job)
        print(job.id)
        return render_template("job_submitted.xhtml", job_id="TODO",
                               submitted_data=request.form,
                               serv_info=get_server_info(q),)


    return redirect(url_for("home_page"), serv_info=get_server_info(q))


@app.route("/status/<job_id>")
def show_status(job_id):
    #TODO: search for job ID
    found = True

    # TODO: get status of the job
    status = "running"

    if found:
        return render_template("status_page.xhtml", job_id=job_id,
                               status=status, serv_info=get_server_info(q))
        # TODO: create status template

    return render_template("not_found.xhtml", job_id=job_id,
                           serv_info=get_server_info(q))
    # TODO: create not_found template


@app.route("/create-database")
def create_database():
    # submitted_data

    return render_template("create_database.xhtml", submit_url=SUBMIT_URL,
                           serv_info=get_server_info(q),
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
                           serv_info=get_server_info(q),
                           session_file_upload=htmlg.SESSION_FILE_UPLOAD,
                           outf_name=htmlg.generate_output_filename_form(
                               "output_name"))

# Error handlers
@app.errorhandler(404)
def invalid_method(error):
    #logging.error(utils.fetch_base_error_message(error, request))
    # return redirect(url_for("home_page"))
    return render_template("page_not_found.xhtml",
                           serv_info=get_server_info(q)), 404


@app.errorhandler(405)
def page_not_found(error):
    base = fetch_base_error_message(error, request)
    #logging.error(f"{base}, METHOD: {request.method}")
    return redirect("home_page")




#print(app.config.keys())
if __name__ == "__main__":
    app.run(debug=True)