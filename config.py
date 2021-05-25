# config settings can be put here

# changable
DEBUG=True

HOST="0.0.0.0"
PORT=5001

SQLALCHEMY_DATABASE_URI = 'sqlite:///status.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DOWNLOAD_FOLDER = "jobs" # multicblaster not required in front of jobs
