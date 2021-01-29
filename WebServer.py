from flask import Flask, request, url_for, redirect, render_template
import utils
import os
import logging
# TODO: Find out how pre-submission uploading works

app = Flask("multicblaster")
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
#logging.basicConfig(filename="logs.log", level=logging.INFO)
SUBMIT_URL = "/submit_job"

@app.route("/")
def home_page():
    return render_template("index.xhtml", submit_url=SUBMIT_URL)

@app.route("/new_job", methods=["GET"])
def new_job():
    return render_template("new_job.xhtml")

@app.route(SUBMIT_URL, methods=["POST"])
def submit_job():
    if request.method == "POST":
        return render_template("job_submitted.xhtml", job_id="TODO",
                               submitted_data=request.form)
    else:
        return redirect(url_for("home_page"))

@app.route("/status/<job_id>")
def show_status(job_id):
    #TODO: search for job ID
    found = True

    # TODO: get status of the job
    status = "running"

    if found:
        return render_template("status_page.xhtml", job_id=job_id,
                               status=status)
        # TODO: create status template

    return render_template("not_found.xhtml", job_id=job_id)
    # TODO: create not_found template

# Error handlers
@app.errorhandler(404)
def invalid_method(error):
    #logging.error(utils.fetch_base_error_message(error, request))
    # return redirect(url_for("home_page"))
    return render_template("page_not_found.xhtml"), 404

@app.errorhandler(405)
def page_not_found(error):
    base = utils.fetch_base_error_message(error, request)
    #logging.error(f"{base}, METHOD: {request.method}")
    return redirect("home_page")


#print(app.config.keys())
if __name__ == "__main__":
    app.run(debug=True)