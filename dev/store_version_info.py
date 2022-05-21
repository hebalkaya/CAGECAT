"""Module to add version info in the database.

Should be run when a new version of CAGECAT is released.

Author: Matthias van den Belt
"""

# package imports
import os
from pip._internal.operations import freeze

# own project imports
from cagecat.db_models import Versions
from cagecat.workers.workers_helpers import run_command
from config_files.config import cagecat_version
from config_files.sensitive import pfam_db_folder
from cagecat import db

### main code
def get_pfam_db_info():
    fp = os.path.join(pfam_db_folder, 'Pfam.version', 'Pfam.version')
    if not os.path.exists(fp):
        cmd = ['tar', '-xf', f'{fp}.gz']
        run_command(
            cmd=cmd,
            log_base=None,
            job_id=None,
            log_output=False
        )

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
