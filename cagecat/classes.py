"""Module to store classes

Author: Matthias van den Belt
"""

import workers as w

function_dict = {'search': w.cblaster_search,
                 'gne': w.cblaster_gne,
                 'extract_sequences': w.cblaster_extract_sequences,
                 'extract_clusters': w.cblaster_extract_clusters,
                 'corason': w.corason,
                 'clinker_full': w.clinker_full,
                 'clinker_query': w.clinker_query}

class CAGECATJob:

    def __init__(self, job_id, options, job_type=None, file_path=None, depending_on=None):
        self.id = job_id
        self.options = options
        self.file_path = file_path
        self.depending = depending_on
        self.set_job_function(job_type)


    def set_job_function(self, job_type):
        if job_type is None:
            self.function = function_dict[self.options['job_type']]
        else:
            self.function = function_dict[job_type]



