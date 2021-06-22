"""Module to remove stored data of jobs that have ran > 30 days ago.

"""
from multicblaster import db
from multicblaster.utils import fetch_job_from_db, JOBS_DIR
from config import CONF
import os
import datetime
import shutil

def get_folders_to_delete(period_to_keep=31):
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
    with open(os.path.join(f'{CONF["MAINTENANCE_LOGS"]}',
                           f'{datetime.datetime.now().date()}_removal.txt'),
              'w') as outf:
        for dir, job_id in get_folders_to_delete():
            shutil.rmtree(dir)
            db.session.delete(fetch_job_from_db(job_id))

            outf.write(f'Deleted: {dir}\n')

    db.session.commit()


if __name__ == '__main__':
    delete_old_jobs()
