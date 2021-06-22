"""Module to remove stored data of jobs that have ran > 30 days ago.

"""
from multicblaster import db
from multicblaster.utils import fetch_job_from_db, JOBS_DIR
import os
import datetime
import shutil


# make list of job_ids which have passed the 30 day mark
# create wrapper function which
    # removes the job_id entry from the SQL db
    # removes the entire folder of a job ID

def get_folders_to_delete(period_to_keep=31):
    to_delete = []
    current = datetime.datetime.now()

    for fn in os.listdir(JOBS_DIR):
        if os.path.isdir(fn):
            if (current - datetime.datetime.fromtimestamp(os.path.getmtime(fn))).days >= period_to_keep:
                to_delete.append((fn, fn.split(os.sep)[-1]))


def delete_old_jobs():

    with open(f'/process_logs/maintenance/{datetime.datetime.now().date()}_removal.txt', 'w') as outf:
        for dir, job_id in get_folders_to_delete():
            shutil.rmtree(dir)
            db.session.delete(fetch_job_from_db(job_id))

            outf.write(f'Deleted: {dir}\n')

    db.session.commit()
