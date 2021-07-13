"""Module to get present databases to be shown for HMMer database selection

Currently, this script is only ran when creating the Docker container, and
should be implemented in a scheduled manner to update the present databases.
TODO: should: see above

Author: Matthias van den Belt
"""

import os
from sys import argv
import typing as t

def list_present_databases(path: str) -> t.List[str]:
    """Lists present databases for HMM searching

    Input:
        - path: path where to search for databases

    Output:
         - _genera: names of genera databases which are present
    """
    # is also in create_databases.py, but
    # added here again to prevent import errors TODO: could: fix

    _genera = []
    for root, _, files in os.walk(path):
        for file in files:
            genus = file.split('.')[0]
            if '_creation' not in genus and genus not in _genera:
                _genera.append(genus)

    return _genera


if __name__ == '__main__':
    if len(argv) == 1 or len(argv) > 2:
        raise IOError(f'Invalid number of arguments: {len(argv)}')

    genera = list_present_databases(argv[1])
    with open('present_databases.txt', 'w') as outf:
        outf.write(','.join(genera))
