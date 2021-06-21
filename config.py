# config settings can be put here

# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///status.db'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# changeable
CONF = {"SQLALCHEMY_DATABASE_URI": 'sqlite:////database.db',
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "DEBUG": True,
        "HOST": "0.0.0.0",
        "PORT": 5001,
        "DOWNLOAD_FOLDER": "jobs",
        "DATABASE_FOLDER": "/lustre/BIF/nobackup/belt017/databases",
        'PFAM_DB_FOLDER': '/pfam_db',
        'MOUNTED_DB_FOLDER': '/hmm_databases',
        "REPRESENTATIVE_GENOMES_THRESHOLD": 50,
        'DOMAIN': 'http://192.168.2.65:5001/',
        'PRESENT_DATABASES_LOCATION': '/present_databases.txt'
        }

EMAIL = {'SMTP_SERVER': 'smtp.gmail.com',
         'SENDER_EMAIL': 'ranberg1892124a2@gmail.com',
         'PASSWORD': '!kjasd2SA2qSA;', # intentionally left out
         }

BASE_URL = 'ftp.ncbi.nlm.nih.gov'
BASE_DIR = '/lustre/BIF/nobackup/belt017/refseq_gbks'
COMPLETE_DOWNLOADS_FILE = '/lustre/BIF/nobackup/belt017/complete_downloads.txt'
SUCCESSFULL_DOWNLOADS_FN = 'successfull_downloads.txt'

# DEBUG=True
#
# HOST="0.0.0.0"
# PORT=5001

# SQLALCHEMY_DATABASE_URI = 'sqlite:///status.db'
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# DOWNLOAD_FOLDER = "jobs" # multicblaster not required in front of jobs
#
# # PFAM_FOLDER = '/lustre/BIF/nobackup/belt017/multicblaster_HMM'
# # DATABASE_FOLDER = '/lustre/BIF/nobackup/belt017/multicblaster_HMM/databases'
# DATABASE_FOLDER = '/storage/databases'
