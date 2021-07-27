"""Module to create HMMer databases

This script should be ran parallel to the download_repr_genomes_wrapper.sh
script, as this script waits for a signal of that script that a database is
ready to be created

Author: Matthias van den Belt

"""
import subprocess
import time
import os
from config_files.config import CONF, BASE_DIR, COMPLETE_DOWNLOADS_FILE
import typing as t

SLEEPING_TIME = 60
CPUS = "10"
BATCH_SIZE = "30"

def init():
    """Creates directories if not present yet

    Output:
        - created directories
    """
    if not os.path.exists(CONF['DATABASE_FOLDER']):
        os.makedirs(CONF['DATABASE_FOLDER'], exist_ok=True)

    os.chdir(CONF['DATABASE_FOLDER'])

    if not os.path.exists('logs'):
        os.mkdir('logs')

def read_contents() -> t.List[str]:
    """Reads file to check if it can create a database from that genus.

    Output:
        - list of genus names

    """
    with open(COMPLETE_DOWNLOADS_FILE) as inf:
        _to_create = [line.strip() for line in inf.readlines()]

    return _to_create


def list_files(_genus: str) -> t.List[str]:
    """Lists all present GenBank files for the given genus

    Input:
        - genus: name of genus to list files for

    Output:
        - list of file paths belonging to the given genus
    """
    all_files = []

    for root, directory, files in os.walk(os.path.join(BASE_DIR, _genus, 'validated')):
        for f in files:
            all_files.append(os.path.join(root, f))

    return all_files


def list_present_databases(path):
    """Lists present databases for HMM searching

    Input:
        - path: path where to search for databases

    Output:
         - genera: names of genera databases which are present
    """
    genera = []
    for root, _, files in os.walk(path):
        for file in files:
            genera.append(file.split('.')[0])

    return genera


if __name__ == '__main__':
    init()

    try:
        while True:
            to_create = read_contents()

            if not to_create:
                print(f'No database to create. Waiting {SLEEPING_TIME} seconds')
                time.sleep(SLEEPING_TIME)
            else:
                for genus in to_create:
                    if genus in list_present_databases(os.getcwd()):
                        print(f'{genus} database already present. Skipped.')
                        continue

                    print(f'Creating {genus} database')

                    # res = subprocess.run(['echo', 'hello'], capture_output=True)
                    cmd = ["cblaster", "makedb", "--name", genus,
                           "--cpus",  CPUS, "--batch", BATCH_SIZE]

                    cmd.extend(list_files(genus))

                    if len(cmd) == 8: # indicates no files were added
                        print(f'{genus} has no genome files. Continueing..')
                        continue

                    with open(os.path.join('logs', f'{genus}_creation.log'), 'w') as outf:
                        res = subprocess.run(cmd, stderr=outf, stdout=outf, text=True)
                    # print(res.stdout)

                    if res.returncode != 0:
                        print('Something went wront. Exiting..')
                        exit(1)

                to_do = []
                for g in read_contents():
                    if g not in to_create:
                        to_do.append(g)

                with open(COMPLETE_DOWNLOADS_FILE, 'w') as outf:
                    for genus in to_do:
                        outf.write(f'{genus}\n')
    except KeyboardInterrupt:
        print('Exiting...')
