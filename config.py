"""Module with changeable parameters if something would change in the future

Author: Matthias van den Belt
"""

# changeable
CONF = {"SQLALCHEMY_DATABASE_URI": 'sqlite:////repo/multicblaster/database.db',
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        # "DEBUG": True,
        # "HOST": "0.0.0.0",
        # "PORT": 5001,
        "DOWNLOAD_FOLDER": "jobs",
        "DATABASE_FOLDER": "/lustre/BIF/nobackup/belt017/databases",
        'PFAM_DB_FOLDER': '/pfam_db',
        'MOUNTED_DB_FOLDER': '/hmm_databases',
        "REPRESENTATIVE_GENOMES_THRESHOLD": 50,
        'DOMAIN': 'http://www.bioinformatics.nl/multicblaster/',
        'PRESENT_DATABASES_LOCATION': '/present_databases.txt',
        'MAINTENANCE_LOGS': '/process_logs/maintenance',
        'SERVER_PREFIX': '/repo',
        'DEV_TEAM_EMAIL': 'matthias.vandenbelt@wur.nl'
        }

# TODO: must: move sensitive information to a separate file and add it to gitignore
EMAIL = {'SMTP_SERVER': 'smtp.gmail.com',
         'SENDER_EMAIL': 'ranberg1892124a2@gmail.com',
         'PASSWORD': '!kjasd2SA2qSA;', # intentionally left out
         'PORT': 465,
         'FOOTER_MSG': '''Thank you for using our service. 

>> If you found this service useful, spread the word.
    
Kind regards,
    
The multicblaster team
https://www.bioinformatics.nl/multicblaster'''
         }

BASE_URL = 'ftp.ncbi.nlm.nih.gov'
BASE_DIR = '/lustre/BIF/nobackup/belt017/refseq_gbks'
COMPLETE_DOWNLOADS_FILE = '/lustre/BIF/nobackup/belt017/complete_downloads.txt'
SUCCESSFULL_DOWNLOADS_FN = 'successfull_downloads.txt'
