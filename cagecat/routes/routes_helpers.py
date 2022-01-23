"""Stores helper functions of the routes.py module

Author: Matthias van den Belt
"""

def format_size(size: int) -> str:
    """Formats the size of a file into MB

    Input:
        - size: size of the a file in bytes

    Output:
        - formatted string showing the size of the file ..MB
    """
    return "%3.1f MB" % (size/1000000) if size is not None else size
