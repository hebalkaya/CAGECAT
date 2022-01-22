from wtforms import Form

from cagecat.form_sections import JobInfoForm, SearchSectionForm, FilteringSectionForm, ClusteringSectionForm, SummaryTableForm, BinaryTableForm, \
    AdditionalOptionsSectionForm, IntermediateGenesSectionForm, SubmitForm, SummaryTableGNEForm, AdditionalOptionsGNEForm, FilteringForm, OutputForm


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
    filtering = FilteringForm()
    output = OutputForm()

    submit = SubmitForm()


class CblasterExtractClustersForm(Form):
    pass

class CblasterVisualisationForm:
    pass

class ClinkerForm:
    pass
