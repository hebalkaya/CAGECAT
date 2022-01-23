"""Stores routes for Flask web application for downstream analyses

Author: Matthias van den Belt
"""

# package imports
from flask import Blueprint, request

# own project imports
from cagecat.tools.tools_helpers import read_headers, parse_selected_cluster_numbers
from cagecat.forms.forms import CblasterSearchForm, CblasterGNEForm, CblasterExtractSequencesForm, \
    CblasterExtractClustersForm, CblasterVisualisationForm, ClinkerDownstreamForm, ClinkerInitialForm
from cagecat.routes.routes import PRESENT_DATABASES
from cagecat.general_utils import show_template, CLUST_NUMBER_PATTERN_W_SCORE, fetch_job_from_db, CLUST_NUMBER_PATTERN_W_CLINKER_SCORE
from cagecat.const import TOOLS_EXPLANATIONS, CLINKER_MODULES, GENBANK_SUFFIXES, FASTA_SUFFIXES
from config_files.config import THRESHOLDS

tools = Blueprint('tools', __name__, template_folder="templates")

### Route function definitions
@tools.route('/')
def tools_page() -> str:
    """Shows page to user showing all available tools

    Output:
        - HTML represented in string format
    """
    return show_template('implemented_tools.html', help_enabled=False)


@tools.route("/explanation")
def tools_explanation() -> str:
    """Shows page for explanation about implemented tools

    Output:
        - HTML represented in string format
    """
    return show_template("tools_explanation.html", help_enabled=False, helps=TOOLS_EXPLANATIONS)


@tools.route("/search/rerun/<prev_run_id>")
@tools.route("/search")
def cblaster_search(prev_run_id: str = None) -> str:
    """Shows home page to the user

    Input:
        - prev_run_id: job ID of a previous run.

    Output:
        - HTML represented in string format

    When the /rerun/<prev_run_id> is visited, the input fields where the user
    can enter previous job IDs are pre-filled with the given job ID
    """
    if "type" in request.args:
        headers = None if prev_run_id is None and request.args["type"] == "recompute" else read_headers(prev_run_id)
        module_to_show = request.args["type"]
    else:
        headers = None
        module_to_show = None

    return show_template("cblaster_search.html",
                                               all_forms=CblasterSearchForm(),
                                               prev_run_id=prev_run_id,
                                               module_to_show=module_to_show,
                                               headers=headers,
                                               genera=PRESENT_DATABASES,
                                               query_file_extensions=','.join(FASTA_SUFFIXES + GENBANK_SUFFIXES),
                                               show_examples='cblaster_search')

@tools.route("/clinker_query", methods=["POST"])
def clinker_query() -> str:
    """Shows page for selecting options to run clinker with query genes

    Output:
        - HTML represented in string format
    """
    clusters = parse_selected_cluster_numbers(
        request.form["selectedClusters"], CLUST_NUMBER_PATTERN_W_SCORE)

    return show_template("cblaster_plot_clusters.html",
                         all_forms=CblasterVisualisationForm(),
                         prev_job_id=request.form["job_id"],
                         cluster_headers=
                         request.form["selectedClusters"].split('\r\n'),
                         selected_clusters=clusters,
                         max_clusters_to_plot=THRESHOLDS['max_clusters_to_plot'])


@tools.route("/extract-sequences", methods=["GET", "POST"])
def extract_sequences() -> str:
    """Shows page for extracting sequences from a previous job

    Input:
        No inputs

    Output:
        - HTML represented in string format showing options for extracting
            sequences in the client's browser
    """
    return show_template("cblaster_extract_sequences.html",
                         all_forms=CblasterExtractSequencesForm(),
                         selected_queries=request.form["selectedQueries"].split('\r\n'),
                         # selected_scaffolds=selected_scaffolds,
                         prev_job_id=request.form["job_id"])

@tools.route("/extract-clusters", methods=["GET", "POST"])
def extract_clusters() -> str:
    """Shows page for extracting clusters from a previous job

    Input:
        No inputs

    Output:
        - HTML represented in string format showing options for extracting
            clusters in the client's browser
    """
    selected_clusters = request.form["selectedClusters"]
    # selected_scaffolds = pa.parse_selected_scaffolds(selected_clusters)
    prev_job_id = request.form["job_id"]
    prev_job = fetch_job_from_db(prev_job_id)

    pattern = CLUST_NUMBER_PATTERN_W_SCORE if \
        fetch_job_from_db(prev_job_id).job_type not in \
        CLINKER_MODULES else \
        CLUST_NUMBER_PATTERN_W_CLINKER_SCORE

    cluster_numbers = parse_selected_cluster_numbers(selected_clusters, pattern)

    return show_template("cblaster_extract_clusters.html",
                         # selected_scaffolds=selected_scaffolds,
                         all_forms=CblasterExtractClustersForm(),
                         cluster_headers=selected_clusters.split('\r\n'),
                         cluster_numbers=cluster_numbers,
                         prev_job_id=prev_job_id, prev_job_type=prev_job.job_type,
                         main_search_id=prev_job.main_search_job,
                         max_clusters_to_extract=config.THRESHOLDS['maximum_clusters_to_extract'])


@tools.route("/corason", methods=["POST"])
def corason() -> str:
    """Shows page for selecting settings for running Corason

    Input:
        No inputs

    Output:
        - HTML represented in string format showing options for running
            Corason in the client's browser
    """
    query = request.form["selectedQuery"]

    selected_clusters = request.form["selectedClusters"].split('\r\n')

    if len(selected_clusters) == 1:
        clust_numbers = parse_selected_cluster_numbers(
            request.form["unselectedClusters"],
            CLUST_NUMBER_PATTERN_W_SCORE, format_nicely=False).split(',')
    else:
        clust_numbers = parse_selected_cluster_numbers(
            request.form["selectedClusters"],
            CLUST_NUMBER_PATTERN_W_SCORE, format_nicely=False).split(',')

    return show_template("corason.html",
                         query=query,
                         cluster_headers=selected_clusters,
                         clust_numbers=clust_numbers,
                         # cluster_to_search_in=cluster_to_search_in,
                         prev_job_id=request.form["job_id"])


@tools.route('/gne', methods=['GET', 'POST'])
def gene_neighbourhood_estimation() -> str:
    return show_template('cblaster_gene_neighbourhood_estimation.html',
                         all_forms=CblasterGNEForm(),
                         max_samples=config.THRESHOLDS['maximum_gne_samples'],
                         prev_job_id=request.form['job_id'])


@tools.route('/clinker', methods=['GET', 'POST'])
def clinker() -> str:
    prev_job_id = None if 'job_id' not in request.form else request.form['job_id']

    if prev_job_id is None:
        form = ClinkerInitialForm()
    else:
        form = ClinkerDownstreamForm()

    return show_template('clinker.html',
                         all_forms=form,
                         query_file_extensions=','.join(GENBANK_SUFFIXES),
                         show_examples='clinker',
                         prev_job_id=prev_job_id)


@tools.route('/big-scape')
def bigscape() -> str:
    return show_template('BiG-SCAPE.html')
