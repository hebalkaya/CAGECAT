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


if __name__ == '__main__':
    init()
    for f in os.listdir():
        print(f)# remove old db's

    print(os.listdir())


# TODO: create script (use other create_database script as example)
# but now we used files created by touch to see which databases should be created

# TODO: compress all refseq gbks
# tar cvf - $fp --remove-files | gzip -9 - > $fp.tar.gz