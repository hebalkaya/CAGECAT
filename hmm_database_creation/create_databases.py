"""Module to create HMMer databases

This script should be ran parallel to the construct_hmm_databases.sh
script, as this script waits for a file, indicating a genus, created by that
script that a database is ready to be created

Author: Matthias van den Belt
"""
import subprocess
import time
import os
import sys
import typing as t

sys.path.append('..')
from config_files.config import CONF, REFSEQ_DIR, CREATE_HMM_DB_SETTINGS

def init():
    """Creates directories if not present yet

    Output:
        - created directories
    """
    if not os.path.exists(CONF['finished_hmm_db_folder']):
        os.makedirs(CONF['finished_hmm_db_folder'], exist_ok=True)

    os.chdir(CONF['finished_hmm_db_folder'])

    if not os.path.exists('logs'):
        os.mkdir('logs')


def list_files(_genus: str) -> t.List[str]:
    """Lists all present GenBank files for the given genus

    Input:
        - genus: name of genus to list files for

    Output:
        - list of file paths belonging to the given genus
    """
    all_files = []

    for root, directory, files in os.walk(os.path.join(REFSEQ_DIR, _genus)):
        for f in files:
            all_files.append(os.path.join(root, f))

    return all_files


if __name__ == '__main__':
    init()
    print('Removing databases')
    for f in os.listdir():
        os.remove(f)
        print(f'  Removed: {f}')# remove old db's

    while True:
        dbs_to_create_path = os.path.join(REFSEQ_DIR, 'databases_to_create')
        dbs_to_create = os.listdir()

        if len(dbs_to_create) == 0:
            print(f'Nothing to create. Sleeping for {CREATE_HMM_DB_SETTINGS["sleeping_time"]} seconds')
            time.sleep(CREATE_HMM_DB_SETTINGS['sleeping_time'])
        elif len(dbs_to_create) == 1 and dbs_to_create[0] == 'stop_creating_databases':
            print('Encountered the stop_creating_databases file.')
            subprocess.run(['rm', os.path.join(dbs_to_create_path, 'stop_creating_databases')])
            print('Finished creating all databases. Exiting')
            exit(0)
        else:
            for genus in dbs_to_create:
                if genus == 'stop_creating_databases':
                    continue  # as we don't want to make a db for this file
                    # actually create the db
                print(f'Creating {genus} database')
                cmd = ["cblaster", "makedb",
                       "--name", genus,
                       "--cpus",  CREATE_HMM_DB_SETTINGS['cpus'],
                       "--batch", CREATE_HMM_DB_SETTINGS['batch_size']]

                cmd.extend(list_files(genus))

                if len(cmd) == 8: # indicates no files were added
                    print(f'{genus} has no genome files. Continuing..')
                    continue

                with open(os.path.join('logs', f'{genus}_creation.log'), 'w') as outf:
                    res = subprocess.run(cmd, stderr=outf, stdout=outf, text=True)

                if res.returncode != 0:
                    print('Something went wrong. Exiting..')
                    exit(1)

                print(f'Successfully created {genus} HMM database')
                subprocess.run(['rm', os.path.join(dbs_to_create_path, genus)])
                print(f'Removed {genus} touch file')

# TODO: create script (use other create_database script as example)
# but now we used files created by touch to see which databases should be created

# TODO: compress all refseq gbks
# tar cvf - $fp --remove-files | gzip -9 - > $fp.tar.gz