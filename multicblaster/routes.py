"""Stores routes for Flask web application

Author: Matthias van den Belt
"""

# import statements
from flask import render_template, request, url_for, redirect, send_file
from multicblaster import app, q, r
import multicblaster.utils as ut
import multicblaster.parsers as pa
import multicblaster.const as co
from multicblaster.models import Job as dbJob
from multicblaster import db
import multicblaster.workers as rf
import os
import copy
from rq.job import Job

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

    print(request.args["type"] if
          "type" in request.args else None)
    return show_template("index.xhtml", submit_url=ut.SUBMIT_URL,
                         prev_run_id=prev_run_id,
                         module_to_show=request.args["type"] if
                         "type" in request.args else None)

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
    print("==== SUBMIT_JOB in ROUTES.PY ====")
    print(request.form)

    print("------args------------------")
    print(request.args)

    new_jobs = []

    job_type = request.form["job_type"]
    job_id = ut.generate_job_id()

    # Note that the "{module}PreviousType" is submitted via the form, but is
    # only used if a previous job ID or previous session file will be used

    ut.create_directories(job_id) # should be done if user uploads files
    # TODO: BIG ONE: make every job_type functional by appending it to the job list
    if job_type == "search":
        f = rf.cblaster_search
        file_path, job_type = prepare_search(job_id, job_type)

        new_jobs.append((f, job_id, request.form, file_path, None, job_type))
    elif job_type == "gne":
        f = rf.cblaster_gne
        file_path = get_previous_job_properties(job_id, job_type, "gne")

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
        # print(request.form)
        f = rf.cblaster_extract_clusters

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

        # print(file_path_extract_clust)

        extr_clust_options = copy.deepcopy(co.EXTRACT_CLUSTERS_OPTIONS)

        merged = "\r\n".join([request.form["selectedClustersToSearch"], request.form["selectedReferenceCluster"]])
        extr_clust_options["clusterNumbers"] = pa.parse_selected_cluster_numbers(merged, ut.CLUST_NUMBER_PATTERN_WITHOUT_SCORE)

        # TODO: extract query sequence
        # query = request.form["selectedQuery"]
        # print(query)
        # new_jobs.append((rf.cblaster_extract_sequences, ut.generate_job_id(), "tmp", file_path_extract_clust, None, "extract_sequences"))

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
        extr_clust_options = copy.deepcopy(co.EXTRACT_CLUSTERS_OPTIONS)
        # TODO: change options?

        file_path_extract_clust = os.path.join(ut.JOBS_DIR, prev_job_id, "results",
                                               f"{prev_job_id}_session.json")
        genome_files_path = os.path.join(ut.JOBS_DIR, job_id, "results")

        new_jobs.append((rf.cblaster_extract_clusters, job_id, extr_clust_options, file_path_extract_clust, None, "extract_clusters"))
        new_jobs.append((rf.clinker_full, ut.generate_job_id(), request.form, genome_files_path, job_id, "clinker_full"))

    elif job_type == "clinker_query":
        prev_job_id = request.form["prev_job_id"]
        file_path = os.path.join(ut.JOBS_DIR, prev_job_id, "results", f"{prev_job_id}_session.json")

        new_jobs.append((rf.clinker_query, job_id, request.form, file_path, None, "clinker_query"))# TODO: depending job could change in future
                # return "should do"

    else: # future input types
        raise NotImplementedError(f"Module {job_type} is not implemented yet in submit_job")

    last_job_id = enqueue_jobs(new_jobs)

    return redirect(url_for("show_result", job_id=last_job_id,
                        pj=ut.fetch_job_from_db(last_job_id).depending_on, store_job_id=True, j_type=ut.fetch_job_from_db(job_id).job_type))


@app.route("/results/<job_id>")
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
            plot_contents, program, size = prepare_finished_result(job_id, module)
            # plot contents is not used

            with open(os.path.join(ut.JOBS_DIR, job_id, "logs",
                                   f"{job_id}_{program}.log")) as inf:
                log_contents = "<br/>".join(inf.readlines())
            # print(ut.get_available_downstream_modules(module))
            return show_template("result_page.xhtml", j_id=job_id,
                                 status=status, content_size=ut.format_size(size), compr_formats=ut.COMPRESSION_FORMATS, module=module,
                                 modules_with_plots=ut.MODULES_WHICH_HAVE_PLOTS,
                                 log_contents=log_contents,
                                 downstream_modules=co.DOWNSTREAM_MODULES_OPTIONS[module])
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
                                 parent_job=pj, status=status, settings=settings, store_job_id=store_job_id, j_type=j_type)
        elif status == "waiting":
            pj = ut.fetch_job_from_db(job_id).depending_on if "pj" not in request.args else request.args["pj"]

            return show_template("status_page.xhtml", j_id=job_id,
                                 status="waiting for preceding job to finish",
                                 settings=settings,
                                 parent_job=pj, store_job_id=store_job_id, j_type=j_type)
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
    else:  # can only be POST as GET and POST are the only allowed methods
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
    cluster_numbers = pa.parse_selected_cluster_numbers(selected_clusters, ut.CLUST_NUMBER_PATTERN_W_SCORE)

    return show_template("extract-clusters.xhtml", submit_url=ut.SUBMIT_URL,
                         selected_scaffolds=selected_scaffolds,
                         cluster_numbers=cluster_numbers,
                         prev_job_id=request.form["job_id"])


@app.route("/downstream/corason", methods=["POST"])
def corason() -> str:
    """Shows page for selecting settings for running Corason

    Input:
        No inputs

    Output:
        - HTML represented in string format showing options for running
            Corason in the client's browser
    """
    # print(request.form)
    cluster_to_search_in = pa.parse_selected_cluster_names(request.form["selectedClusters"])
    query = request.form["selectedQuery"]
    reference_cluster = pa.parse_selected_cluster_names(request.form["selectedReferenceCluster"])

    return show_template("corason.xhtml", submit_url=ut.SUBMIT_URL,
                         query=query, reference_cluster=reference_cluster,
                         cluster_to_search_in=cluster_to_search_in,
                         prev_job_id=request.form["job_id"])


@app.route("/downstream/clinker")
def full_clinker() -> str:

    return show_template("full_clinker.xhtml", submit_url=ut.SUBMIT_URL)


@app.route("/downstream/clinker_query", methods=["POST"])
def clinker_query() -> str:
    # print("===== ROUTES.PY CLINKER_QUERY.PY =====")
    # print(request.form)
    selected_scaffolds = pa.parse_selected_scaffolds(
        request.form["selectedClusters"])

    clusters = pa.parse_selected_cluster_numbers(request.form["selectedClusters"], ut.CLUST_NUMBER_PATTERN_W_SCORE)

    return show_template("clinker_query.xhtml", submit_url=ut.SUBMIT_URL,
                         prev_job_id=request.form["job_id"],
                         selected_scaffolds=selected_scaffolds,
                         selected_clusters= clusters)

@app.route("/downstream")
def post_analysis_explanation() -> str:
    return show_template("post_analysis_explanation.xhtml")


@app.route("/plots/<job_id>")
def get_plot_contents(job_id) -> str:
    return prepare_finished_result(job_id, ut.fetch_job_from_db(job_id).job_type)[0]


@app.route("/help")
def help_page():
    # TODO: actually create
    return show_template("help.xhtml")


@app.route("/docs/<input_type>")
def get_help_text(input_type):
    if input_type not in co.HELP_TEXTS:
        return show_template("page_not_found.xhtml", stat_code=404)

    return co.HELP_TEXTS[input_type]


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

        ut.check_valid_job(prev_job_id, job_type)

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

    return file_path, job_type


def prepare_finished_result(job_id: str,
                            module: str) -> t.Tuple[t.Union[str, None], str, t.Union[int, None]]:
    """Returns HTML code of plots if applicable and appropriate program

    Input:
        - job_id: ID corresponding to the job the results are requested for
        - module: module type of given job id for which the results are
            requested

    Output:
        - plot_contents: HTML code of a plot
        - program: the program that was executed by this job
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
        program = "echo"  # TODO: will be someting else later
        plot_contents = None  # TODO: for now

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


def enqueue_jobs(new_jobs: t.List[t.Tuple[t.Callable, str,
                                          "TODO", t.Union[str, None],
                                          t.Union[str, None], str]]) -> str:
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

    Output:
        - last_job_id: job ID of the last added job. Used to show appropriate
            results page and fetch a job which this job depends on, if
            applicable
    """
    if len(new_jobs) == 0:
        raise IOError("Submitted a job, but no job added to the list")

    created_redis_jobs_ids = []

    for i, new_job in enumerate(new_jobs):
        ut.create_directories(new_job[1])
        ut.save_settings(new_job[2], new_job[1])

        # depends_on kwarg could be None if it is not dependent.
        depending_job = None if new_job[4] is None else \
            created_redis_jobs_ids[i-1][1]

        job = q.enqueue(new_job[0], args=(new_job[1],),
                        kwargs={"options": new_job[2],
                                "file_path": new_job[3]},
                        depends_on=depending_job,
                        result_ttl=86400)

        status = "queued" if depending_job is None else "waiting"
        # for parent job to finish

        j = dbJob(id=new_job[1], status=status, job_type=new_job[5],
                  redis_id=job.id,
                  depending_on="null" if
                  depending_job is None else new_job[4])  # is our own job ID

        db.session.add(j)
        db.session.commit()

        created_redis_jobs_ids.append((new_job[1], job.id)) # own ID, redis id

        last_job_id = new_job[1]

    return last_job_id


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
