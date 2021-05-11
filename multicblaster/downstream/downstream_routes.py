from flask import Blueprint, request
import multicblaster.parsers as pa
import multicblaster.utils as ut
from multicblaster.routes import show_template

downstream = Blueprint('downstream', __name__, template_folder="templates")

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