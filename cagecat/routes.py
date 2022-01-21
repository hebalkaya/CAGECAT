"""Stores routes for Flask web application

Author: Matthias van den Belt
"""

# package imports
from flask import request, url_for, redirect
import os
import copy

# own project imports
import cagecat.help_texts
from cagecat import app
import cagecat.utils as ut
import cagecat.const as co
import cagecat.routes_helpers as rthelp
from cagecat.classes import CAGECATJob
from cagecat.forms import JobInfoForm
from config_files.config import CAGECAT_VERSION, CONF

global PRESENT_DATABASES
# route definitions

@app.route('/cagecat')
def home_page_old_url():
    return redirect(url_for('home_page'))

@app.route('/')
def home_page():
    return rthelp.show_template('index.html', help_enabled=False)


@app.route(co.SUBMIT_URL, methods=["POST"])
def submit_job() -> str:
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
    if request.method == 'POST':
        form = JobInfoForm(request.form)
        # print(form.title)
        print(form.mail_address)

        if not form.validate():
            print(form.errors)

        print(form)
        print(form.validate())
        print(form.errors)

    new_jobs = []

    job_type = request.form["job_type"]
    job_id = ut.generate_job_id()

    # Note that the "{module}PreviousType" is submitted via the form, but is
    # only used if a previous job ID or previous session file will be used

    ut.create_directories(job_id)

    if job_type == "search":
        file_path, job_type = rthelp.prepare_search(job_id, job_type)
        print('Line 55 job type', job_type)

        new_jobs.append(CAGECATJob(job_id=job_id,
                                   options=request.form,
                                   job_type=job_type,
                                   file_path=file_path))

    elif job_type == "gne":
        new_jobs.append(CAGECATJob(job_id=job_id,
                                   options=request.form,
                                   file_path=rthelp.get_previous_job_properties(job_id, job_type, "gne")))

    elif job_type == "extract_sequences":
        # For now, only when coming from a results page (using a previous job
        # id) is supported

        new_jobs.append(CAGECATJob(job_id=job_id,
                                   options=request.form,
                                   file_path=os.path.join(ut.JOBS_DIR,
                                              request.form['prev_job_id'],
                                              "results",
                                              f"{request.form['prev_job_id']}_session.json")))

    elif job_type == "extract_clusters":
        prev_job_id = ut.fetch_job_from_db(
            request.form["prev_job_id"]).main_search_job

        if prev_job_id == "null":
            prev_job_id = request.form["prev_job_id"]
        # For now, only when coming from a results page (using a previous job
        # id) is supported

        new_jobs.append(CAGECATJob(job_id=job_id,
                                   options=request.form,
                                   file_path=os.path.join(ut.JOBS_DIR,
                                              prev_job_id,
                                              "results",
                                              f"{prev_job_id}_session.json")))

    # elif job_type == "corason":
    #     extr_clust_options = copy.deepcopy(co.EXTRACT_CLUSTERS_OPTIONS)
    #     clust_numbers = dict(request.form)
    #
    #     extr_clust_options['clusterNumbers'] = \
    #         clust_numbers['selectedClustersToUse'] + f' {request.form["selectedReferenceCluster"]}' # as we also need the cluster file for the reference bgc
    #
    #     # TODO future: extract query sequence
    #
    #     new_jobs.append(CAGECATJob(job_id=job_id,
    #                                options=extr_clust_options,
    #                                job_type='extract_clusters',
    #                                file_path=os.path.join(ut.JOBS_DIR,
    #                                       request.form['prev_job_id'],
    #                                       "results",
    #                                       f"{request.form['prev_job_id']}_session.json")))
    #
    #     new_jobs.append(CAGECATJob(job_id=ut.generate_job_id(),
    #                                options=request.form,
    #                                file_path='TODOCORASONPATH',
    #                                depends_on_job_id=new_jobs[-1].job_id))  # get the last CAGECATJob object
    #
    #     # TODO future: file path corason --> for corason, the file path is the path to where the extracted clusters will be

    elif job_type == "clinker":
        if 'clinkerEnteredJobId' in request.form:  # indicates it was downstream
            prev_job_id = request.form["clinkerEnteredJobId"]

            if ut.fetch_job_from_db(prev_job_id).job_type == 'extract_clusters':
                genome_files_path = os.path.join(ut.JOBS_DIR, prev_job_id, "results")
                depending_on = None
            else:
                new_jobs.append(CAGECATJob(job_id=job_id,
                                           options=copy.deepcopy(co.EXTRACT_CLUSTERS_OPTIONS),
                                           job_type='extract_clusters',
                                           file_path=os.path.join(ut.JOBS_DIR,
                                                                  prev_job_id,
                                                                  "results",
                                                                  f"{prev_job_id}_session.json")))

                genome_files_path = os.path.join(ut.JOBS_DIR, job_id, "results")
                depending_on = new_jobs[-1].job_id

        elif request.files:  # started as individual tool
            for f in request.files.getlist('fileUploadClinker'):
                if f.filename:
                    ut.save_file(f, job_id)
                    genome_files_path = os.path.join(ut.JOBS_DIR, job_id, "uploads")
                else: # indicates the example was posted
                    genome_files_path = os.path.join('cagecat', 'example_files')
            depending_on = None

        else:
            raise ValueError('Incorrect submitted options (clinker)')

        new_jobs.append(CAGECATJob(job_id=job_id if depending_on is None else ut.generate_job_id(),
                                   options=request.form,
                                   file_path=genome_files_path,
                                   depends_on_job_id=depending_on))

    elif job_type == "clinker_query":
        new_jobs.append(CAGECATJob(job_id=job_id,
                                   options=request.form,
                                   file_path=os.path.join(ut.JOBS_DIR,
                                          request.form['prev_job_id'],
                                          "results",
                                          f"{request.form['prev_job_id']}_session.json")))

    else:  # future input types
        raise NotImplementedError(f"Module {job_type} is not implemented yet in submit_job")

    last_job = ut.fetch_job_from_db(rthelp.enqueue_jobs(new_jobs))

    url = url_for("result.show_result",
                  job_id=last_job.id,
                  pj=last_job.depending_on,
                  store_job_id=True,
                  job_title=last_job.title,
                  email=last_job.email,
                  j_type=last_job.job_type)

    return rthelp.show_template('redirect.html', url=url)


@app.route("/help")
def help_page() -> str:
    """Shows the help page to the user

    Output:
        - HTML represented in string format
    """
    return rthelp.show_template("help.html", version=CAGECAT_VERSION, help_enabled=False)


@app.route("/docs/<input_type>")
def get_help_text(input_type):
    """Returns help text corresponding to the requested input parameter

    Input:
        - input_type: HTML name of the input parameter

    Output:
        - help texts of input parameter. Keys: "title", "module", "text"
    """

    if input_type not in cagecat.help_texts.HELP_TEXTS:
        return {'title': 'Missing help text', 'module': '', 'text':
            'This help text is missing. Please submit feedback and indicate'
            ' of which parameter the help text is missing.\n\nThanks in advance.'}

    return cagecat.help_texts.HELP_TEXTS[input_type]


@app.route('/server-status')
def get_server_status():
    return rthelp.get_server_info()


@app.route('/update-hmm-databases')
def update_hmm_databases():
    global PRESENT_DATABASES
    # Doesn't have to return anything, only trigger
    genera = []

    for f in os.listdir(CONF['finished_hmm_db_folder']):
        genus = f.split('.')[0]
        if genus not in genera:
            genera.append(genus)

    PRESENT_DATABASES = genera

    return '1'  # indicating everything went well


# Error handlers
@app.errorhandler(404)
def page_not_found(error):  # should have 1 parameter, doesn't have to be used
    """Shows page displaying that the requested page was not found

    """
    return rthelp.show_template("page_not_found.html",
                                stat_code=404,
                                help_enabled=False)


@app.errorhandler(405)
def invalid_method():
    """Redirects user to home page if method used for request was invalid

    """
    return redirect(url_for("home_page"))


update_hmm_databases()
# within routes.py to prevent circular import (as it was first in const.py).
# Additionally, this variable does not have to be updated manually, and
# is therefore left out of const.py
