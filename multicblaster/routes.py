"""Stores routes for Flask web application

Author: Matthias van den Belt
"""

# package imports
from flask import request, url_for, redirect
import os
import copy

# own project imports
from typing import Dict

from multicblaster import app
import multicblaster.utils as ut
import multicblaster.parsers as pa
import multicblaster.const as co
import multicblaster.routes_helpers as rthelp
import multicblaster.workers as rf
import multicblaster.const as const

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
    if "type" in request.args:
        headers = None if prev_run_id is None and request.args["type"] == "recompute" else ut.read_headers(prev_run_id)
        module_to_show = request.args["type"]
    else:
        headers = None
        module_to_show = None

    return rthelp.show_template("index.xhtml",
                                submit_url=ut.SUBMIT_URL,
                                prev_run_id=prev_run_id,
                                module_to_show=module_to_show,
                                headers=headers, genera=const.PRESENT_DATABASES)


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
    # TODO: create a class for job
    new_jobs = []

    job_type = request.form["job_type"]
    job_id = ut.generate_job_id()

    # Note that the "{module}PreviousType" is submitted via the form, but is
    # only used if a previous job ID or previous session file will be used

    ut.create_directories(job_id)
    # TODO: BIG ONE: make every job_type functional by appending it to the job list
    if job_type == "search":
        f = rf.cblaster_search
        file_path, job_type = rthelp.prepare_search(job_id, job_type)

        new_jobs.append((f, job_id, request.form, file_path, None, job_type))

    elif job_type == "gne":
        f = rf.cblaster_gne
        file_path = rthelp.get_previous_job_properties(job_id, job_type, "gne")

        new_jobs.append((f, job_id, request.form, file_path, None, job_type))

    elif job_type == "extract_sequences":
        # For now, only when coming from a results page (using a previous job
        # id) is supported
        f = rf.cblaster_extract_sequences

        prev_job_id = request.form["prev_job_id"]
        file_path = os.path.join(ut.JOBS_DIR, prev_job_id, "results",
                                 f"{prev_job_id}_session.json")

        new_jobs.append((f, job_id, request.form, file_path, None, job_type))

    elif job_type == "extract_clusters":
        f = rf.cblaster_extract_clusters

        prev_job_id = ut.fetch_job_from_db(request.form["prev_job_id"]).main_search_job
        if prev_job_id == "null":
            prev_job_id = request.form["prev_job_id"]

        file_path = os.path.join(ut.JOBS_DIR, prev_job_id, "results",
                                 f"{prev_job_id}_session.json")
        # For now, only when coming from a results page (using a previous job
        # id) is supported

        new_jobs.append((f, job_id, request.form, file_path, None, job_type))

    elif job_type == "corason":
        prev_job_id = request.form["prev_job_id"]
        file_path_extract_clust = os.path.join(ut.JOBS_DIR, prev_job_id, "results",
                               f"{prev_job_id}_session.json")

        extr_clust_options = copy.deepcopy(co.EXTRACT_CLUSTERS_OPTIONS)

        merged = "\r\n".join([request.form["selectedClustersToSearch"], request.form["selectedReferenceCluster"]])
        extr_clust_options["clusterNumbers"] = pa.parse_selected_cluster_numbers(merged, ut.CLUST_NUMBER_PATTERN_WITHOUT_SCORE)

        # TODO: extract query sequence

        corason_job_id = ut.generate_job_id()
        new_options = dict(request.form)

        # save antismash file. Empty string indicates no file was uploaded
        if request.files["antismashFile"].filename != "":
            ut.create_directories(corason_job_id)
            new_options["antismashFile"] = ut.save_file(
                request.files["antismashFile"], corason_job_id)

        new_jobs.append((rf.cblaster_extract_clusters, job_id, extr_clust_options, file_path_extract_clust, None, "extract_clusters"))
        new_jobs.append((rf.corason, corason_job_id, new_options, "CORASONPATHTODO", job_id, "corason"))

        # TODO: file path corason --> for corason, the file path is the path to where the extracted clusters will be

    elif job_type == "clinker_full":
        prev_job_id = request.form["clinkerEnteredJobId"]
        prev_job = ut.fetch_job_from_db(prev_job_id)


        if prev_job.job_type == 'extract_clusters':
            genome_files_path = os.path.join(ut.JOBS_DIR, prev_job_id, "results")
            depending_job = None
        else:
            extr_clust_options = copy.deepcopy(co.EXTRACT_CLUSTERS_OPTIONS)
            # TODO: change options?

            file_path_extract_clust = os.path.join(ut.JOBS_DIR, prev_job_id, "results",
                                                   f"{prev_job_id}_session.json")
            new_jobs.append((rf.cblaster_extract_clusters, job_id, extr_clust_options, file_path_extract_clust, None, "extract_clusters"))

            genome_files_path = os.path.join(ut.JOBS_DIR, job_id, "results")
            depending_job = job_id

        new_jobs.append((rf.clinker_full, ut.generate_job_id(), request.form, genome_files_path, depending_job, "clinker_full"))

    elif job_type == "clinker_query":
        prev_job_id = request.form["prev_job_id"]
        file_path = os.path.join(ut.JOBS_DIR, prev_job_id, "results", f"{prev_job_id}_session.json")

        new_jobs.append((rf.clinker_query, job_id, request.form, file_path, None, "clinker_query"))  # TODO: depending job could change in future

    else:  # future input types
        raise NotImplementedError(f"Module {job_type} is not implemented yet in submit_job")


    last_job_id = rthelp.enqueue_jobs(rthelp.add_title_email_to_job(
        new_jobs, request.form))

    last_job = ut.fetch_job_from_db(last_job_id)
    # print(last_job)
    url = url_for("result.show_result",
                  job_id=last_job_id,
                  pj=last_job.depending_on,
                  store_job_id=True,
                  job_title=last_job.title,
                  email=last_job.email,
                  j_type=last_job.job_type)
    print(url)
    print(url[14:])
    return rthelp.show_template('redirect.xhtml', url=url)


@app.route("/help")
def help_page() -> str:
    """Shows the help page to the user

    Output:
        - HTML represented in string format
    """
    # TODO: actually create
    return rthelp.show_template("help.xhtml", help_enabled=False)


@app.route("/docs/<input_type>")
def get_help_text(input_type):
    """Returns help text corresponding to the requested input parameter

    Input:
        - input_type: HTML name of the input parameter

    Output:
        - help texts of input parameter. Keys: "title", "module", "text"
    """

    if input_type not in co.HELP_TEXTS:
        ##### TODO: REMOVE LATER BETWEEN LINES: DEVELOPMENT PURPOSES #####
        with open('not_registered_helps.txt', "r+") as outf:
            all_unregistrered_helps = [line.strip() for line in outf.readlines()]
            # print(all_unregistrered_helps)

            if input_type not in all_unregistrered_helps:
                outf.write(f"{input_type}\n")
        ##### UNTIL HERE #####

        return rthelp.show_template("page_not_found.xhtml", stat_code=404)

    return co.HELP_TEXTS[input_type]


# Error handlers
@app.errorhandler(404)
def page_not_found():
    """Shows page displaying that the requested page was not found

    """
    return rthelp.show_template("page_not_found.xhtml", stat_code=404)


@app.errorhandler(405)
def invalid_method():
    """Redirects user to home page if method used for request was invalid

    """
    return redirect(url_for("home_page"))


@app.route("/testing")
def testing():
    # TODO: remove
    html = """<script>let var1 = 0;function a(){var1 += 1; document.getElementById('counter').textContent = var1; console.log(document.getElementById('counter'));
    console.log("hi");window.postMessage("This is the actual message", "*");}</script><span id="counter" style="color: white">0</span>
    <button id="TestingSomething" onclick="a()">Testerrr</>
    """

    html = """<script>let var1 = 0;function a(){var1 += 1; document.getElementById('counter').textContent = var1;parent.window.postMessage("how should", "*");}</script><span id="counter" style="color: white">0</span>
    <button id="TestingSomething" onclick="a()">Testerrr</>
    """

    with open(r"test_runs\tester.html") as inf:
        html = inf.read()

    return rthelp.show_template("testing.xhtml", html_contents=html)

@app.route("/jala")
def ani_tester():
    return rthelp.show_template('ani_tester.xhtml')
