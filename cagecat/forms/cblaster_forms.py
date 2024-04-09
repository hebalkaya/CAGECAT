from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField, RadioField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import StringField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class CblasterSearchForm(FlaskForm):
    # Job description fields
    job_title = StringField('Job title', validators=[DataRequired()], render_kw={"placeholder": "experiment name or number"})
    institution_name = StringField('Institution name', validators=[DataRequired()], render_kw={"placeholder": "institution name"})
    email_address = EmailField('Email address (notifications)', validators=[DataRequired(), Email()], render_kw={"placeholder": "username@institution.com"})

    # Search fields
    entrez_query = StringField('Entrez query', validators=[DataRequired()], render_kw={"placeholder": "Aspergillus[organism]"})
    database = SelectField('Database', choices=[('nr', 'RefSeq non-redundant proteins (nr)'), ('refseq_protein', 'RefSeq protein'), ('swissprot', 'Swissprot'), ('custom', '[Custom Database] Streptomyces_complete')])
    maximum_hits = IntegerField('Maximum hits', validators=[DataRequired()], default=500)

    # Intermediate genes fields
    find_intermediate_genes = BooleanField('Find intermediate genes', id='find_intermediate_genes')
    maximum_distance = IntegerField('Maximum distance', id='maximum_distance', default=5000)
    maximum_clusters = IntegerField('Maximum clusters', id='maximum_clusters', default=100)

    # Input type fields
    input_type = RadioField('Input Type', choices=[
        ('remote', 'Remote'),
        ('hmm', 'HMM'),
        ('remote_hmm', 'Remote+HMM'),
        ('mibig', 'MIBiG 3.1'),
        ('antismash', 'antiSMASH 4.0')
    ], default='remote')

    # Remote input type fields
    remote_input_type = RadioField('Input Type', choices=[
        ('file', 'File'),
        ('ncbi_entries', 'NCBI Entries')
    ], default='file')

    # Define a StringField for the text box
    database_entry = StringField('Database entry', validators=[DataRequired()], render_kw={"placeholder": "BGC 000"})

    # Advanced fields
    # Filtering fields
    max_e_value = FloatField('Maximum e-value', id='max_e_value', default=0.01)
    min_identity = IntegerField('Minimum identity (%)', id='min_identity', default=30)
    min_query_coverage = IntegerField('Minimum query coverage (%)', id='min_query_coverage', default=50)
    # Clustering fields
    max_intergenic_gap = IntegerField('Maximum intergenic gap', id='max_intergenic_gap', default=20000)
    min_presence_percentage = IntegerField('Minimum gene presence % in clusters', id='min_presence_percentage', default=0)
    min_unique_hits = IntegerField('Minimum unique hits', id='min_unique_hits', default=3)
    min_cluster_hits = IntegerField('Minimum cluster hits', id='min_cluster_hits', default=3)
    required_sequences = StringField('Required sequences', id='required_sequences')
    # Summary table fields
    summary_delimiter = StringField('Delimiter', id='summary_delimiter', default="-")
    summary_decimal = IntegerField('Decimals', id='summary_decimals', default=2)
    summary_hide_header = BooleanField('Hide summary table header', id='summary_hide_header')
    # Binary table fields
    binary_delimiter = StringField('Delimiter', id='binary_delimiter', default="-")
    binary_decimal = IntegerField('Decimals', id='binary_decimals', default=2)
    binary_hide_header = BooleanField('Hide binary table header', id='binary_hide_header')
    key_function = SelectField('Key function', choices=[('len', 'Length (len)'), ('sum', 'Summation (sum)'), ('max', 'Maximum (max)')])
    hit_attribute = SelectField('Hit attribute', choices=[('identity', 'Identity'), ('coverage', 'Coverage'), ('bitscore', 'Bit-score'), ('evalue', 'E-value')])
    # Additional field
    sort_clusters = RadioField('Sort clusters', id='sort_clusters')

    # Submit button
    submit = SubmitField('Submit')
