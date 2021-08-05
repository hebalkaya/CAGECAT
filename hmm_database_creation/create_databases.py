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
import shutil
import requests

sys.path.append('..')
from config_files.config import CONF, REFSEQ_DIR, CREATE_HMM_DB_SETTINGS

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
    print('Removing databases', flush=True)

    os.chdir(CONF['finished_hmm_db_folder'])
    for f in os.listdir():
        try:
            os.remove(f)
        except IsADirectoryError:
            shutil.rmtree(f)

        print(f'  Removed: {f}', flush=True)  # remove old db's

    path = os.path.join(CONF['finished_hmm_db_folder'], 'logs')
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    while True:
        dbs_to_create_path = os.path.join(REFSEQ_DIR, 'databases_to_create')
        dbs_to_create = os.listdir(dbs_to_create_path)

        if len(dbs_to_create) == 0:
            print(f'Nothing to create. Sleeping for {CREATE_HMM_DB_SETTINGS["sleeping_time"]} seconds', flush=True)
            time.sleep(CREATE_HMM_DB_SETTINGS['sleeping_time'])
        elif len(dbs_to_create) == 1 and dbs_to_create[0] == 'stop_creating_databases':
            print('Encountered the stop_creating_databases file', flush=True)
            subprocess.run(['rm', os.path.join(dbs_to_create_path, 'stop_creating_databases')])
            print('Finished creating all databases.', flush=True)

            res = requests.get('https://www.bioinformatics.nl/cagecat/update-hmm-databases')

            if res.text == '1':
                print('Successfully updated the available databases variable in the back-end, which is used to create the front-end')
            else:
                print('Something did not go well when updating the available databases')

            exit(0)
        else:
            for genus in dbs_to_create:
                if genus == 'stop_creating_databases':
                    continue  # as we don't want to make a db for this file
                    # actually create the db
                print(f'Creating {genus} database', flush=True)
                cmd = ["cblaster", "makedb",
                       "--name", genus,
                       "--cpus",  CREATE_HMM_DB_SETTINGS['cpus'],
                       "--batch", CREATE_HMM_DB_SETTINGS['batch_size']]

                cmd.extend(list_files(genus))

                if len(cmd) == 8: # indicates no files were added
                    print(f'{genus} has no genome files. Continuing..', flush=True)
                    continue

                with open(os.path.join(CONF['finished_hmm_db_folder'], 'logs', f'{genus}_creation.log'), 'w') as outf:
                    res = subprocess.run(cmd, stderr=outf, stdout=outf, text=True)

                if res.returncode != 0:
                    print('Something went wrong. Exiting..', flush=True)
                    exit(1)

                print(f'  Successfully created {genus} HMM database', flush=True)
                subprocess.run(['rm', os.path.join(dbs_to_create_path, genus)])
                print(f'  Removed {genus} touch file', flush=True)


# TODO future: we could compress all refseq gbks until the next time we use it so we save storage
# example command:
# tar cvf - $fp --remove-files | gzip -9 - > $fp.tar.gz
