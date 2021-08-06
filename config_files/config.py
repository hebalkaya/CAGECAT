"""Module with changeable parameters if something would change in the future

Author: Matthias van den Belt
"""
CAGECAT_VERSION = '1.09'

# jobs to persist on server (i.e. example outputs)
PERSISTENT_JOBS = ('W885A828D304Y06',
                   'N250X793I290S34',
                   'K814Y501M103S02')

# changeable
CONF = {"SQLALCHEMY_DATABASE_URI": 'sqlite:////repo/cagecat/database.db',
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        'PFAM_DB_FOLDER': '/pfam_db',
        'finished_hmm_db_folder': '/hmm_databases',
        'DOMAIN': 'http://www.bioinformatics.nl/cagecat/',
        'MAINTENANCE_LOGS': '/process_logs/maintenance',
        'SERVER_PREFIX': '/repo',
        }

CREATE_HMM_DB_SETTINGS = {'sleeping_time': 60,
                          'cpus': '10',
                          'batch_size': '30'}

THRESHOLDS = {
    'maximum_clusters_to_extract': 150,
    'maximum_gne_samples': 300,
    'max_clusters_to_plot': 75,
    "representative_genomes_number": 50
}

EMAIL = {'smtp_server': 'smtp.wur.nl',
         'sender_email': 'cage.cat@wur.nl',  # is also the dev team email
         'port': 25,
         'footer_msg': '''Thank you for using our service. 

>> If you found this service useful, spread the word.
    
Kind regards,
    
The CAGECAT team
https://www.bioinformatics.nl/cagecat'''
         }

NCBI_FTP_BASE_URL = 'ftp.ncbi.nlm.nih.gov'
REFSEQ_DIR = '/hmm_db_downloads'
