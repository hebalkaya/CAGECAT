"""Module to add version info in the database.

Should be run when a new version of CAGECAT is released.

Should be run from within the /repo/maintenance folder. If a virtualenviroment is
activated, deactivate it by running

conda deactivate

Author: Matthias van den Belt
"""

# package imports
import os
import sys
from pathlib import Path

from pip._internal.operations import freeze

sys.path.append('..')

# own project imports
from cagecat.db_utils import Versions
from cagecat.workers.workers_helpers import run_command
from config_files.config import cagecat_version
from config_files.sensitive import pfam_db_folder
from cagecat import db

### main code
def get_pfam_db_info():
    fp = Path(pfam_db_folder, 'Pfam.version')
    if not fp.exists():
        cmd = ['gunzip', str(Path(pfam_db_folder, 'Pfam.version.gz'))]

        return_code = run_command(cmd=cmd, job_id=None, log_output=False)
        if return_code != 0:
            raise ValueError(f'Non-zero return code encountered: {return_code}')

    with open(fp) as inf:
        info = inf.read()

    return info

if __name__ == "__main__":
    entry = Versions(
        cagecat_version=cagecat_version,
        pip=';'.join(list(freeze.freeze())),
        pfam=get_pfam_db_info()
    )

    db.session.add(entry)
    db.session.commit()
