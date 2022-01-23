from wtforms import Form

from cagecat.form_sections import JobInfoForm, SearchSectionForm, FilteringSectionForm, ClusteringSectionForm, SummaryTableForm, BinaryTableForm, \
    AdditionalOptionsSectionForm, IntermediateGenesSectionForm, SubmitForm, SummaryTableGNEForm, AdditionalOptionsGNEForm, \
    ExtractSequencesFilteringForm, ExtractSequencesOutputForm, ExtractClustersOutputForm, ClustersFilteringForm, \
    CblasterVisualisationOutputForm, ClinkerAlignmentForm, ClinkerOutputForm, ClinkerAdditionalOptionsForm


class GeneralForm(Form):
    """Has job info and submit input fields

    """
    job_info = JobInfoForm()
    submit = SubmitForm()

class CblasterSearchForm(Form):
    general = GeneralForm()
    search = SearchSectionForm()
    filtering = FilteringSectionForm()
    clustering = ClusteringSectionForm()
    summary_table = SummaryTableForm()
    binary_table = BinaryTableForm()
    additional_options = AdditionalOptionsSectionForm()
    intermediate_genes = IntermediateGenesSectionForm()


class CblasterRecomputeForm(Form):
    pass

class CblasterGNEForm(Form):
    general = GeneralForm()
    summary_table = SummaryTableGNEForm()
    additional_options = AdditionalOptionsGNEForm()

class CblasterExtractSequencesForm(Form):
    general = GeneralForm()
    filtering = ExtractSequencesFilteringForm()
    output = ExtractSequencesOutputForm()

class CblasterExtractClustersForm(Form):
    general = GeneralForm()
    filtering = ClustersFilteringForm()
    output = ExtractClustersOutputForm()

class CblasterVisualisationForm(Form):
    general = GeneralForm()
    filtering = ClustersFilteringForm()
    output = CblasterVisualisationOutputForm()

class ClinkerBaseForm(Form):
    general = GeneralForm()
    alignment = ClinkerAlignmentForm()
    output = ClinkerOutputForm()
    additional_options = ClinkerAdditionalOptionsForm()

class ClinkerDownstreamForm(Form):
    base = ClinkerBaseForm()

class ClinkerInitialForm(Form):
    general = GeneralForm()
