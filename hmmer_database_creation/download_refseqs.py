"""Module which downloads RefSeqs from the NCBI database

Author: Matthias van den Belt
"""

import hashlib
import os
import subprocess
import ftplib
import time
from sys import argv
import typing as t

from config import *
import create_databases as cr


def init() -> str:
    """Fetches FTP paths of input genus

    Input:
        - No input

    Output:
        - output_fn: name of output file
    Uses the fetch_ftp_paths.sh script
    """
    print(f'\nStarting: {argv[1].capitalize()}\n')

    genus = argv[1].capitalize()
    output_fn = f'{genus}_ftp_paths.txt'

    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
        print(f'Created directory {BASE_DIR}')

    print(f'Fetching FTP paths (writing to {output_fn})')
    subprocess.run(['bash', 'get_ftp_paths.sh', genus, output_fn])
    print('\t-> success')

    return output_fn


def parse_paths(ftp_paths_fn: str, ext='.gbff.gz') -> \
        t.Dict[str, t.Tuple[str, str, str]]:
    """Parses the paths downloaded by the fetch_ftp_paths.sh script

    Input:
        - ftp_paths_fn: filename where ftp paths are stored

    Output:
        - list of tuples of parsed ftp paths which can be used to directly
            download the corresponding file
            [0] = base ftp path for that genus
            [1] = GenBank suffix filename to point to the GenBank file
            [2] = md5 suffix filename to point to the md5-checksum file
    """
    all_paths = {}

    if not os.path.exists(ftp_paths_fn):
        raise IOError('No hits found. Did you make a spelling error?')

    with open(ftp_paths_fn) as inf:
        all_lines = inf.readlines()

    for line in all_lines:
        splitted = line.strip().split()
        path, genus, species = splitted[0], splitted[1], " ".join(splitted[2:])
        key = ' '.join([genus, species])

        paths = (path, f'{path.split("/")[-1]}_genomic{ext}', f'md5checksums.txt')

        if key in all_paths:
            key += '1'

        all_paths[key] = paths

    return all_paths


def create_dir(*args) -> str:
    """Creates directory if it does not exist yet. Recursive.

    Input:
        - unknown number of string parameters

    Output:
        - names: full path name
    """
    names = os.path.join(*args)
    if not os.path.exists(names):
        os.makedirs(names, exist_ok=True)
        print(f'\t-> created directory {names}')

    return names


def validate_file(gb_path: str, name,
                  incorrect_entries_fn='incorrect_entries.txt'):
    """Validates GenBank file using their md5-checksum

    Input:
        - gb_path: path to GenBank file
        - name: genus name

    Output:
        - logging to output files (either successful or incorrect)
    """
    genus = name.split()[0]
    successful_downloads_fn = f'{genus}_{SUCCESSFUL_DOWNLOADS_FN}'

    with open(os.path.join(BASE_DIR, 'md5checksums.txt')) as inf:
        for line in inf.readlines():
            splitted = line.strip().split()
            if splitted[-1].endswith('genomic.gbff.gz'):
                ori_chksum = splitted[0]
                break

    with open(os.path.join(BASE_DIR, gb_path), 'rb') as inf:
        calc_chksum = hashlib.md5(inf.read()).hexdigest()

    if calc_chksum == ori_chksum:
        print('\t-> validated')

        subprocess.run(['gzip', '-d', os.path.join(BASE_DIR, gb_path)])
        print('\t-> unzipped')

        p = create_dir(BASE_DIR, genus, 'validated')

        # move file from downloading folder to appropriate genus folder
        os.rename(os.path.join(BASE_DIR, gb_path[:-3]), os.path.join(BASE_DIR, p, gb_path[:-3]))
        print(f'\t-> moved to {p}')

        with open(successful_downloads_fn, 'w' if not os.path.exists(successful_downloads_fn) else 'a') as outf:
            outf.write(f'{name}:{gb_path[:-3]}\n')
    else:
        with open(incorrect_entries_fn, 'w' if not os.path.exists(incorrect_entries_fn) else 'a') as outf:
            outf.write(f'{gb_path}\n')

        print(f'\t-> failed (written to {incorrect_entries_fn})')


def download_files(paths: t.Tuple[str, str, str], blocksize=33554432):
    """Downloads GenBank and md5-checksums files from NCBI FTP sites

    Sleeping steps are to not overload NCBI's servers: we are only allowed to
    perform 3 requests per seconds.

    Input:
        - paths: see documentation on parse_paths()

    Output:
        - downloaded, validated GenBank files
    """
    total = len(paths)
    for count, (key, value) in enumerate(paths.items(), start=1):
        print(f'({count}/{total}): {key}')
        base, gb_path, md5_path = value
        if check_if_already_downloaded(key):
            print('\t-> skipped (already downloaded)')
            continue

        ftp = ftplib.FTP(BASE_URL)

        time.sleep(0.34)
        ftp.login()

        time.sleep(0.34)
        ftp.cwd('/'.join(base[5:].split('/')[2:]))

        for counter, f in enumerate((gb_path, md5_path), start=1):
            print(f'\t-> downloading ({counter}/{2})')
            time.sleep(0.34)
            with open(os.path.join(BASE_DIR, f), 'wb') as outf:
                ftp.retrbinary(f'RETR {f}', outf.write, blocksize=blocksize)

        validate_file(gb_path, key)


def check_if_already_downloaded(name):
    # TODO: can probably be removed when this is going to be a scheduled re-download
    # TODO: or not, as the script might fail due to NCBI, and we don't want to start all over again, so we could start from this point again
    everything = {}

    if not os.path.exists('successfully_downloaded.txt'):
        with open('successfully_downloaded.txt', 'w') as outf:
            pass

    fn = f'{name.split()[0]}_{SUCCESSFUL_DOWNLOADS_FN}'
    if os.path.exists(fn):
        with open(fn) as inf:
            for entry in inf.readlines():
                splitted = entry.strip().split(':')
                everything[splitted[0]] = splitted[1]

    return name in everything



def check_if_already_has_too_few_species():
    # TODO: can probably be removed when this is going to be a scheduled re-download
    # TODO: or not, as the script might fail due to NCBI, and we don't want to start all over again, so we could start from this point again
    with open('too_few_species.txt') as inf:
        genera = [g.strip().split()[0] for g in inf.readlines()]

    if argv[1].capitalize() in genera:
        print(f'Skipping {argv[1].capitalize()}: (known: too few species)')
        exit(0)


def check_if_db_already_exists():
    # TODO: can probably be removed when this is going to be a scheduled re-download
    # TODO: or not, as the script might fail due to NCBI, and we don't want to start all over again, so we could start from this point again
    if argv[1] in cr.list_present_databases(CONF['DATABASE_FOLDER']):
        print(f'{argv[1].capitalize()} database already present. Skipped.')
        exit(0)  # exit as this script is ran individually for each genus


if __name__ == '__main__':
    check_if_already_has_too_few_species()
    check_if_db_already_exists()

    fn = init()
    paths = parse_paths(fn)
    species_count = len(paths.values())
    if species_count < CONF['REPRESENTATIVE_GENOMES_THRESHOLD']:
        print(f'Skipping {argv[1].capitalize()} genus. ({species_count} species < { CONF["REPRESENTATIVE_GENOMES_THRESHOLD"]})')
        with open('too_few_species.txt', 'w' if not os.path.exists('too_few_species.txt') else 'a') as outf:
            outf.write(f'{argv[1].capitalize()} {species_count}\n')
        exit(0)

    download_files(paths)

    with open(COMPLETE_DOWNLOADS_FILE, 'w' if not os.path.exists(
            COMPLETE_DOWNLOADS_FILE) else 'a') as outf:
        outf.write(f'{argv[1].capitalize()}\n')

    print(f"\nAll done!")
