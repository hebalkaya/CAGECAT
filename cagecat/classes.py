"""Module to store classes

Author: Matthias van den Belt
"""

import cagecat.workers as w

function_dict = {'search': w.cblaster_search,
                 'gne': w.cblaster_gne,
                 'extract_sequences': w.cblaster_extract_sequences,
                 'extract_clusters': w.cblaster_extract_clusters,
                 'corason': w.corason,
                 'clinker_full': w.clinker_full,
                 'clinker_query': w.clinker_query}

class CAGECATJob:
    # TODO: documentation

    def __init__(self, job_id, options, job_type=None, file_path=None, depends_on_job_id=None):
        self.job_id = job_id
        self.options = options
        self.file_path = file_path
        self.depends_on_job_id = depends_on_job_id
        self.function = function_dict[self.options['job_type']] \
            if job_type is None else function_dict[job_type]

        self.title = options['job_title'] if 'job_title' in options else None
        self.email = options['email'] if 'email' in options else None


    def get_job_type(self):
        return self.options['job_type']



