"""Stores routes for Flask web application

Author: Matthias van den Belt
"""

# import statements
from flask import render_template, request, url_for, redirect, send_file
from multicblaster import app, q, r
import multicblaster.utils as ut
import multicblaster.parsers as pa
from multicblaster.models import Job
from multicblaster import db
import multicblaster.workers as rf
import os

# type imports
import flask.wrappers
import typing as t

# !!!! TODO: Note that the return types could change when deploying Flask !!!!

# route definitions



@app.route("/rerun/<prev_run_id>")
@app.route("/")
def home_page(prev_run_id: str = None) -> str:
    """Shows home page to the user

    Input:
        - prev_run_id: job ID of a previous run.

    Output:
        - HTML represented in string format

    When the /rerun/<prev_run_id> is visited, the input fields where the user
    can enter previous job IDs are pre-filled with the given job ID
    """
    return show_template("index.xhtml", submit_url=ut.SUBMIT_URL, prev_run_id=prev_run_id)

@app.route(ut.SUBMIT_URL, methods=["POST"])
def submit_job():  # return type: werkzeug.wrappers.response.Response:
    """Handles job submissions by putting it onto the Redis queue

    Input:
        No inputs

    Output:
        - redirect to results page of the generated job ID

    Raises:
        - NotImplementedError: when functionality that has not been implented
            yet is called.
        - IOError: failsafe for when for some reason no jobID or sessionFile
            was given
    """
    # print(request.form)

    job_type = request.form["job_type"]
    job_id = ut.generate_job_id()

    # Note that the "{module}PreviousType" is submitted via the form, but is
    # only used if a previous job ID or previous session file will be used

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

                file_path = os.path.join(ut.JOBS_DIR, prev_job_id, "results", f"{prev_job_id}_session.json")

            elif file_type == "sessionFile":
                file_path = ut.save_file(request.files["searchUploadedSessionFile"], job_id)
            else:
                raise IOError("Not valid file type")
    elif job_type == "gne":
        f = rf.cblaster_gne

        file_type = request.form["gnePreviousType"]

        if file_type == "jobID":
            prev_job_id = request.form["gneEnteredJobId"]

            ut.check_valid_job(prev_job_id, job_type)

            file_path = os.path.join(ut.JOBS_DIR, prev_job_id, "results", f"{prev_job_id}_session.json")
        elif file_type == "sessionFile":
            file_path = ut.save_file(request.files["gneUploadedSessionFile"], job_id)
        else:
            raise IOError("Not valid file type")
    elif job_type == "extract_sequences":
        # For now, only when coming from a results page (using a previous job
        # id) is supported
        f = rf.cblaster_extract_sequences

        prev_job_id = request.form["prev_job_id"]
        file_path = os.path.join(ut.JOBS_DIR, prev_job_id, "results",
                                 f"{prev_job_id}_session.json")

    elif job_type == "extract_clusters":
        # print(request.form)
        f = rf.cblaster_extract_clusters

        prev_job_id = request.form["prev_job_id"]
        file_path = os.path.join(ut.JOBS_DIR, prev_job_id, "results",
                                 f"{prev_job_id}_session.json")
        # For now, only when coming from a results page (using a previous job
        # id) is supported
    else: # future input types
        raise NotImplementedError(f"Module {job_type} is not implemented yet")

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
def show_result(job_id: str) -> str:
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

            if module == "extract_sequences" or module == "extract_clusters":
                plot_contents = None
            elif module == "search" or module == "recompute":
                with open(os.path.join(ut.JOBS_DIR, job_id,
                                       "results", f"{job_id}_plot.html")) as inf:
                    plot_contents = inf.read()
            else:
                raise NotImplementedError(f"Module {module} has not been implemented yet")

            with open(os.path.join(ut.JOBS_DIR, job_id,
                                       "logs", f"{job_id}_cblaster.log")) as inf:
                log_contents = "<br/>".join(inf.readlines())

            return show_template("result_page.xhtml", job_id=job_id,
                    status=status, compr_formats=ut.COMPRESSION_FORMATS,
                    plot_contents=plot_contents, module=module,
                    select_cluster_modules=ut.MODULES_CLUSTER_SELECTION, log_contents=log_contents)
        elif status == "failed":
            with open(os.path.join(ut.JOBS_DIR, job_id,
                                   "logs", f"{job_id}_cblaster.log")) as inf:
                log_contents = "<br/>".join(inf.readlines())

            return show_template("failed_job.xhtml", settings=settings,
                                 job_id=job_id, log_contents=log_contents)
        elif status == "queued" or status == "running":
            return show_template("status_page.xhtml", job_id=job_id,
                                 status=status, settings=settings)
        else:
            raise IOError(f"Incorrect status of job {job_id} in database")

    else: # indicates no such job exists in the database
        return show_template("job_not_found.xhtml", job_id=job_id)
        # TODO: create not_found template

@app.route("/download-results/<job_id>", methods=["POST"])
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

    if len(submitted_data) != 2: # should be job_id and compression_type
        return redirect(url_for("home_page"))

    compr_type = submitted_data["compression_type"]

    # TODO: first, execute compression_conversion script
    # to go from ours server-default compression to the desired compresion
    # format

    # TODO: send_from_directory is a safer approach, but this suits for now
    # as Flask should not be serving files when deployed
    return send_file(os.path.join(app.config["DOWNLOAD_FOLDER"],
                                  job_id, "results", f"{job_id}.zip"))


@app.route("/results", methods=["GET", "POST"])
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
        return show_template("result_from_jobid.xhtml")
        # return render_template("result_from_jobid.xhtml", serv_info=ut.get_server_info(q, r))
    else: # method is POST
        job_id = request.form["job_id"]
        if ut.fetch_job_from_db(job_id) is not None:
            return redirect(url_for('show_result', job_id=job_id))
        else:
            return show_template("job_not_found.xhtml", job_id=job_id)
            #TODO: create invalid job ID template


@app.route("/downstream/extract-sequences", methods=["GET", "POST"])
def extract_sequences() -> str:
    """Shows page for extracting sequences from a previous job

    Input:
        No inputs

    Output:
        - HTML represented in string format showing options for extracting
            sequences in the client's browser
    """
    selected_queries = request.form["selectedQueries"]
    selected_scaffolds = pa.parse_selected_scaffolds(
        request.form["selectedClusters"])

    if selected_queries == "No queries selected":
        selected_queries = None

    return show_template("extract-sequences.xhtml", submit_url=ut.SUBMIT_URL,
                         selected_queries=selected_queries,
                         selected_scaffolds=selected_scaffolds,
                         prev_job_id=request.form["job_id"])


@app.route("/downstream/extract-clusters", methods=["GET", "POST"])
def extract_clusters() -> str:
    """Shows page for extracting clusters from a previous job

    Input:
        No inputs

    Output:
        - HTML represented in string format showing options for extracting
            clusters in the client's browser
    """
    selected_clusters = request.form["selectedClusters"]
    selected_scaffolds = pa.parse_selected_scaffolds(selected_clusters)
    cluster_numbers = pa.parse_selected_cluster_numbers(selected_clusters)

    return show_template("extract-clusters.xhtml", submit_url=ut.SUBMIT_URL,
                         selected_scaffolds=selected_scaffolds,
                         cluster_numbers=cluster_numbers,
                         prev_job_id=request.form["job_id"])


@app.route("/downstream/corason", methods=["POST"])
def corason():
    print(request.form)
    return show_template("corason.xhtml")


# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    return show_template("page_not_found.xhtml", stat_code=404)


@app.errorhandler(405)
def invalid_method(error):
    return redirect(url_for("home_page"))


# auxiliary functions
def show_template(template_name: str, stat_code=None, **kwargs) \
        -> t.Union[str, t.Tuple[str, int]]:
    """Returns rendered templates to the client

    Input:
        - template_name: name of template to be rendered. By default,
            templates should be located in the templates/ folder
        - stat_code, int: HTTP status code to be returned to the client
        - kwargs: keyword arguments used during rendering of the template

    Output:
        - rendered template (HTML code) represented in string format

    Function was created to prevent redundancy when getting the server info
    and uses Flask's render_template function to actually render the templates
    """
    if stat_code is None:
        return render_template(template_name,
                               serv_info=ut.get_server_info(q, r), **kwargs)
    else:
        return render_template(template_name,
                               serv_info=ut.get_server_info(q, r),
                               **kwargs), stat_code


@app.route("/testing")
def testing():
    html = """<script>let var1 = 0;function a(){var1 += 1; document.getElementById('counter').textContent = var1; console.log(document.getElementById('counter'));
    console.log("hi");window.postMessage("This is the actual message", "*");}</script><span id="counter" style="color: white">0</span>
    <button id="TestingSomething" onclick="a()">Testerrr</>
    """

    html = """<script>let var1 = 0;function a(){var1 += 1; document.getElementById('counter').textContent = var1;parent.window.postMessage("how should", "*");}</script><span id="counter" style="color: white">0</span>
    <button id="TestingSomething" onclick="a()">Testerrr</>
    """

    with open(r"test_runs\tester.html") as inf:
        html = inf.read()

    return show_template("testing.xhtml", html_contents=html)



























