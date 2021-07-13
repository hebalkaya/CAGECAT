"""Module to remove stored data of jobs that have ran > 30 days ago.

Author: Matthias van den Belt
"""
from multicblaster import db
from multicblaster.utils import fetch_job_from_db, JOBS_DIR
from config import CONF
import os
import datetime
import shutil

import typing as t

# Function definitions
def get_folders_to_delete(period_to_keep: int = 31) -> t.List[t.Tuple[str, str]]:
    """Returns the folders which are too old to keep (and should be deleted)

    Input:
        - period_to_keep: how many days files should be stored on the server

    Output:
        - to_delete: directory path and job ID's to delete
    """

    to_delete = []
    current = datetime.datetime.now()
    j_dir = os.path.join(CONF['SERVER_PREFIX'], JOBS_DIR)

    for fn in os.listdir(j_dir):
        fp = os.path.join(j_dir, fn)
        if os.path.isdir(fp):
            if (current - datetime.datetime.fromtimestamp(os.path.getmtime(fp))).days >= period_to_keep:
                to_delete.append((fp, os.path.split(fp)[-1]))

    return to_delete


def delete_old_jobs():
    """Delete old jobs from the server

    Output:
        - None, entries are removed from the database and job folders which
            have expired the storage data are removed
    """
    with open(os.path.join(f'{CONF["MAINTENANCE_LOGS"]}',
                           f'{datetime.datetime.now().date()}_removal.txt'),
              'w') as outf:
        for directory, job_id in get_folders_to_delete():
            shutil.rmtree(directory)
            db.session.delete(fetch_job_from_db(job_id))

            outf.write(f'Deleted: {directory}\n')

    db.session.commit()


if __name__ == '__main__':
    delete_old_jobs()
