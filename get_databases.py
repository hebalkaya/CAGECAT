import os
from sys import argv

def list_present_databases(path): # is also in create_databases.py, but
    # added here again to prevent import errors: TODO: fix
    genera = []
    for root, dir, files in os.walk(path):
            for file in files:
                genus = file.split('.')[0]
                if '_creation' not in genus and genus not in genera:
                        genera.append(genus)

    return genera

if __name__ == '__main__':
    if len(argv) == 1 or len(argv) > 2:
        raise IOError(f'Invalid number of arguments: {len(argv)}')


    genera = list_present_databases(argv[1])
    with open('present_databases.txt', 'w') as outf:
        outf.write(','.join(genera))