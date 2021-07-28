"""Module to get present databases to be shown for HMMer database selection

Currently, this script is only ran when creating the Docker container, and
should be implemented in a scheduled manner to update the present databases.
TODO: should: see above

Author: Matthias van den Belt
"""

from sys import argv
from hmmer_database_creation.create_databases import list_present_databases

if __name__ == '__main__':
    if len(argv) == 1 or len(argv) > 2:
        raise IOError(f'Invalid number of arguments: {len(argv)}')

    genera = list_present_databases(argv[1])

    # probably this output file path should be changed
    with open('present_databases.txt', 'w') as outf:
        outf.write(','.join(genera))
