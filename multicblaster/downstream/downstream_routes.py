"""TODO: docstring


"""

# package imports
from flask import Blueprint, request

# own project imports
import multicblaster.parsers as pa
import multicblaster.utils as ut
from multicblaster.routes_helpers import show_template

downstream = Blueprint('downstream', __name__, template_folder="templates")

### Route function definitions
@downstream.route("/downstream")
def post_analysis_explanation() -> str:
    """Shows page for explanation about post analysis modules

    Output:
        - HTML represented in string format
    """
    return show_template("post_analysis_explanation.xhtml", help_enabled=False)


@downstream.route("/clinker_query", methods=["POST"])
def clinker_query() -> str:
    """Shows page for selecting options to run clinker with query genes

    Output:
        - HTML represented in string format
    """
    selected_scaffolds = pa.parse_selected_scaffolds(
        request.form["selectedClusters"])

    # print(request.form['selectedClusters'])
    clusters = pa.parse_selected_cluster_numbers(
        request.form["selectedClusters"], ut.CLUST_NUMBER_PATTERN_W_SCORE)

    return show_template("clinker_query.xhtml",
                         submit_url=ut.SUBMIT_URL,
                         prev_job_id=request.form["job_id"],
                         cluster_headers=
                         request.form["selectedClusters"].split('\r\n'),
                         selected_clusters=clusters)


@downstream.route("/extract-sequences", methods=["GET", "POST"])
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

@downstream.route("/extract-clusters", methods=["GET", "POST"])
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
    prev_job = request.form["job_id"]

    pattern = ut.CLUST_NUMBER_PATTERN_W_SCORE if \
        ut.fetch_job_from_db(prev_job).job_type not in \
        ('clinker_query', 'clinker_full') else \
        ut.CLUST_NUMBER_PATTERN_W_CLINKER_SCORE
    # TODO: store the now hardcoded clinker_modules in a constant

    cluster_numbers = pa.parse_selected_cluster_numbers(selected_clusters,
                                                        pattern)

    return show_template("extract-clusters.xhtml", submit_url=ut.SUBMIT_URL,
                         selected_scaffolds=selected_scaffolds,
                         cluster_numbers=cluster_numbers,
                         prev_job_id=prev_job)


@downstream.route("/corason", methods=["POST"])
def corason() -> str:
    """Shows page for selecting settings for running Corason

    Input:
        No inputs

    Output:
        - HTML represented in string format showing options for running
            Corason in the client's browser
    """
    # cluster_to_search_in = pa.parse_selected_cluster_names(
    #     request.form["selectedClusters"])
    # print(cluster_to_search_in)

    # reference_cluster = pa.parse_selected_cluster_names(
    #     request.form["selectedReferenceCluster"])

    query = request.form["selectedQuery"]

    return show_template("corason.xhtml", submit_url=ut.SUBMIT_URL,
                         query=query,
                         cluster_headers=
                         request.form["selectedClusters"].split('\r\n'),
                         # cluster_to_search_in=cluster_to_search_in,
                         prev_job_id=request.form["job_id"])
