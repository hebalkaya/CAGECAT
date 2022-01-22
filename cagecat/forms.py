from wtforms import Form

from cagecat.form_sections import JobInfoForm, SearchSectionForm, FilteringSectionForm, ClusteringSectionForm, SummaryTableForm, BinaryTableForm, \
    AdditionalOptionsSectionForm, IntermediateGenesSectionForm, SubmitForm


class CblasterSearchForm(Form):
    job_info = JobInfoForm()
    search = SearchSectionForm()
    filtering = FilteringSectionForm()
    clustering = ClusteringSectionForm()
    summary_table = SummaryTableForm()
    binary_table = BinaryTableForm()
    additional_options = AdditionalOptionsSectionForm()
    intermediate_genes = IntermediateGenesSectionForm()
    submit = SubmitForm()
