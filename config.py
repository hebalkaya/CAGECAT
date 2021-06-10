# config settings can be put here

# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///status.db'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# changeable
CONF = {"SQLALCHEMY_DATABASE_URI": 'sqlite:///status.db',
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "DEBUG": True,
        "HOST": "0.0.0.0",
        "PORT": 5001,
        "DOWNLOAD_FOLDER": "jobs",
        "DATABASE_FOLDER": "/lustre/BIF/nobackup/belt017/databases",
        "REPRESENTATIVE_GENOMES_THRESHOLD": 50,
        'DOMAIN': 'http://192.168.2.65:5001/'
        }

EMAIL = {'SMTP_SERVER': 'smtp.gmail.com',
         'SENDER_EMAIL': 'ranberg1892124a2@gmail.com',
         'PASSWORD': '', # intentionally left out
         }
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