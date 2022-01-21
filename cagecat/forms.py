import wtforms
from wtforms import StringField, EmailField, HiddenField, SelectField, IntegerField, DecimalField, SelectMultipleField, BooleanField, SubmitField
from wtforms import Form, validators as val

# name and id are set to the variable name
# description equals the corresponding help text word
from cagecat.valid_input_cblaster import is_safe_string, is_safe_string_value


cblaster_search_databases = [
    ('nr', 'nr'),
    ('refseq_protein', 'Refseq protein'),
    ('swissprot', 'Swissprot'),
    ('pdbaa', 'pdbaa')
]

cblaster_search_binary_table_key_functions = [
    ('len', 'len'),
    ('sum', 'sum'),
    ('max', 'max')
]

cblaster_search_binary_table_hit_attributes = [
    ('identity', 'identity'),
    ('coverage', 'coverage'),
    ('bitscore', 'bitscore'),
    ('evalue', 'evalue')
]

class SubmitForm(Form):
    submit = SubmitField(
        default='Submit',
        render_kw={
            'class': 'button'
        }
    )


class JobInfoForm(Form):
    job_title = StringField(
        label=u'Job title',
        validators=[val.length(max=60), is_safe_string_value],
        description='job_title'
    )

    mail_address = EmailField(
        label=u'Email address for notification',
        validators=[val.length(max=100)],
        description='email_notification'
    )

class SearchSectionForm(Form):
    entrez_query = StringField(
        label=u'Entrez query',
        validators=[is_safe_string_value],
        description='entrez_query',
        render_kw={
            'placeholder': 'Aspergillus[organism]'
        }
    )

    database_type = SelectField(
        # TODO: when other values than choices are posted, check if it raises error
        label=u'Database',
        validators=[val.input_required(), is_safe_string_value],
        description='database_type',
        choices=cblaster_search_databases,
        render_kw={
            'class': 'select-options'
        }
    )

    hitlist_size = IntegerField(
        label=u'Maximum hits',
        validators=[val.input_required(), is_safe_string_value],
        description='max_hits',
        default=500,
        id='max_hits',
        render_kw={
            'min': 1,
            'max': 10000,
            'step': 1
        }
    )

class FilteringSectionForm(Form):
    max_evalue = DecimalField(
        label=u'Max. e-value',
        validators=[val.input_required(), is_safe_string_value],
        description='max_evalue',
        default=0.01,
        render_kw={
            'min': 0.01,
            'max': 100,
            'step': 0.01
        }
    )

    min_identity = IntegerField(
        label=u'Min. identity (%)',
        validators=[val.input_required(), is_safe_string_value],
        description='min_identity',
        default=30,
        render_kw={
            'min': 0,
            'max': 100,
            'step': 1
        }
    )

    min_query_coverage = IntegerField(
        label=u'Min. query coverage (%)',
        validators=[val.input_required(), is_safe_string_value],
        description='min_query_coverage',
        default=50,
        render_kw={
            'min': 0,
            'max': 100,
            'step': 1
        }
    )

class ClusteringSectionForm(Form):
    max_intergenic_gap = IntegerField(
        label=u'Max. intergenic gap',
        validators=[val.input_required(), is_safe_string_value],
        description='max_intergenic_gap',
        default=20000,
        render_kw={
            'min': 0,
            'max': 1000000,
            'step': 1
        }
    )

    percentageQueryGenes = IntegerField(
        label=u'Percentage',
        validators=[val.input_required(), is_safe_string_value],
        description='percentageQueryGenes',
        default=50,
        render_kw={
            'min': 0,
            'max': 100,
            'step': 1
        }
    )

    min_unique_query_hits = IntegerField(
        label=u'Min. unique query hits',
        validators=[val.input_required(), is_safe_string_value],
        description='min_unique_query_hits',
        default=3,
        render_kw={
            'min': 0,
            'max': 150,
            'step': 1
        }
    )

    min_hits_in_clusters = IntegerField(
        label=u'Min. hits in clusters',
        validators=[val.input_required(), is_safe_string_value],
        description='min_hits_in_clusters',
        default=3,
        render_kw={
            'min': 0,
            'max': 150,
            'step': 1
        }
    )

    requiredSequencesSelector = SelectMultipleField(
        label=u'Required sequences',
        validators=[is_safe_string_value],
        description='requiredSequencesSelector',
        render_kw={
            'style': 'width: 60%;'
        }
    )

    requiredSequences = HiddenField(
        validators=[is_safe_string_value],
        render_kw={
            'value': ''
        }
    )

def get_table_form(module: str, table_type: str):

    prefix = f'{module}{table_type}'

    delimiter = StringField(
        label=u'Delimiter',
        validators=[val.length(max=1), is_safe_string_value],
        description='generalDelimiter',
        id=f'{prefix}TableDelim',
        name=f'{prefix}TableDelim',
        render_kw={
            'size': 1,
            'class': 'short'
        }
    )

    decimals = IntegerField(
        label=u'Decimals',
        validators=[val.input_required(), is_safe_string_value],
        description='generalDecimals',
        default=2,
        id=f'{prefix}TableDecimals',
        name=f'{prefix}TableDecimals',
        render_kw={
            'min': 0,
            'max': 9,
            'step': 1,
            'class': 'short'
        }
    )

    hide_headers = BooleanField(
        label=u'Hide headers',
        validators=[is_safe_string_value], # TODO: add boolean validators
        description='generalHideHeaders',
        id=f'{prefix}TableHideHeaders',
        name=f'{prefix}TableHideHeaders'
    )

    return delimiter, decimals, hide_headers


class SummaryTableForm(Form):
    delimiter, decimals, hide_headers = get_table_form('search', 'Sum')


class BinaryTableForm(Form):
    delimiter, decimals, hide_headers = get_table_form('search', 'Bin')

    keyFunction = SelectField(
        label=u'Key function',
        validators=[val.input_required(), is_safe_string_value],
        description='keyFunction',
        choices=cblaster_search_binary_table_key_functions,
        render_kw={
            'onChange': 'changeHitAttribute()',
            'class': 'select-options'
        }
    )

    hitAttribute = SelectField(
        label=u'Hit attribute',
        validators=[val.input_required(), is_safe_string_value],
        description='hitAttribute',
        choices=cblaster_search_binary_table_hit_attributes,
        render_kw={
            'disabled': '',
            'class': 'select-options'
        }
    )


class AdditionalOptionsSectionForm(Form):
    sortClusters = BooleanField(
        label=u'Sort clusters',
        validators=[is_safe_string_value], # TODO: add boolean validator
        description='sortClusters'
    )

class IntermediateGenesSectionForm(Form):
    intermediate_genes = BooleanField(
        label=u'Find intermediate genes',
        validators=[is_safe_string_value], # TODO: add boolean validator
        description='intermediate_genes',
        render_kw={
            'onclick': "toggleDisabled('intermediate_max_distance', 'intermediate_max_clusters')"
        }
    )

    intermediate_max_distance = IntegerField(
        label=u'Max. distance',
        validators=[is_safe_string_value],
        description='intermediate_max_distance',
        default=5000,
        render_kw={
            'min': 0,
            'max': 250000,
            'disabled': ''
        }
    )

    intermediate_max_clusters = IntegerField(
        label=u'Max. clusters',
        validators=[is_safe_string_value],
        description='intermediate_max_clusters',
        default=100,
        render_kw={
            'min': 1,
            'max': 100,
            'disabled': ''
        }
    )





    # TODO: multiple selection form: https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.SelectMultipleField





class JobTypeForm(Form):
    prev_job_id = HiddenField()

    pass

class PreviousJob(JobTypeForm):
    pass
