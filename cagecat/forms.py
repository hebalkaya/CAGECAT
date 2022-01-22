from wtforms import Form

from cagecat.form_sections import JobInfoForm, SearchSectionForm, FilteringSectionForm, ClusteringSectionForm, SummaryTableForm, BinaryTableForm, \
    AdditionalOptionsSectionForm, IntermediateGenesSectionForm, SubmitForm, SummaryTableGNEForm, AdditionalOptionsGNEForm, \
    ExtractSequencesFilteringForm, ExtractSequencesOutputForm, ExtractClustersOutputForm, ExtractClustersFilteringForm


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

class CblasterRecomputeForm(Form):

    pass

class CblasterGNEForm(Form):
    job_info = JobInfoForm()
    summary_table = SummaryTableGNEForm()
    additional_options = AdditionalOptionsGNEForm()
    submit = SubmitForm()

class CblasterExtractSequencesForm(Form):
    job_info = JobInfoForm()
    filtering = ExtractSequencesFilteringForm()
    output = ExtractSequencesOutputForm()
    submit = SubmitForm()

class CblasterExtractClustersForm(Form):
    job_info = JobInfoForm()
    filtering = ExtractClustersFilteringForm()
    output = ExtractClustersOutputForm()
    submit = SubmitForm()

class CblasterVisualisationForm:
    pass

class ClinkerForm:
    pass
