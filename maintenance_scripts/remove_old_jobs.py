"""Module to remove stored data of jobs that have ran > 30 days ago.

"""
from multicblaster import db
from multicblaster.utils import fetch_job_from_db

# make list of job_ids which have passed the 30 day mark
# create wrapper function which
    # removes the job_id entry from the SQL db
    # removes the entire folder of a job ID


db.session.delete(fetch_job_from_db(j_id))
db.session.commit()