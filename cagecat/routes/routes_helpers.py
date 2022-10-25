"""Stores helper functions of the routes.py module

Author: Matthias van den Belt
"""
from cagecat.general_utils import show_template


def format_size(size: int) -> str:
    """Formats the size of a file into MB

    Input:
        - size: size of a file in bytes

    Output:
        - formatted string showing the size of the file in MB
    """
    return "%3.1f MB" % (size/1000000) if size is not None else size


def show_invalid_submission(errors):
    return show_template('invalid_submission.html', errors=errors, help_enabled=False, stat_code=422)
