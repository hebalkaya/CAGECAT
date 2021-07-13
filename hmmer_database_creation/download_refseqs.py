import hashlib
import os
import subprocess
import ftplib
import time
from sys import argv

from config import *
import create_databases as cr

# genus = 'Streptomyces'
# term = f'(((prokaryota[orgn] AND ("representative genome"[refseq category] OR "reference genome"[refseq category])) AND (latest[filter] AND all[filter] NOT anomalous[filter]))) AND {genus}[Organism]'


def init():
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

def write_error(key, paths, db, error_fn='errors.txt'):
    print(f'Duplicate of {key} (written to {error_fn})')
    with open(error_fn, 'w' if os.path.exists(error_fn) else 'a') as outf:
        outf.write(f'{key}:{paths}-{db[key]}')


def parse_paths(ftp_paths_fn, ext='.gbff.gz'):
    all_paths = {}

    if not os.path.exists(ftp_paths_fn):
        raise IOError('No hits found. Did you make a spelling error?')

    with open(ftp_paths_fn) as inf:
        all_lines = inf.readlines()

    for line in all_lines:
        # print(line)
        # print(line.strip().split())
        splitted = line.strip().split()
        path, genus, species = splitted[0], splitted[1], " ".join(splitted[2:])
        key = ' '.join([genus, species])

        paths = (path, f'{path.split("/")[-1]}_genomic{ext}', f'md5checksums.txt')

        if key in all_paths:
            key += '1'

        all_paths[key] = paths

    return all_paths


def create_dir(*args):
    names = os.path.join(*args)
    if not os.path.exists(names):
        os.makedirs(names, exist_ok=True)
        print(f'\t-> created directory {names}')

    return names


def validate_file(gb_path, name,
                  incorrect_entries_fn='incorrect_entries.txt',
                  ):
    genus = name.split()[0]
    successfull_downloads_fn = f'{genus}_{SUCCESSFULL_DOWNLOADS_FN}'

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

        os.rename(os.path.join(BASE_DIR, gb_path[:-3]), os.path.join(BASE_DIR, p, gb_path[:-3]))
        print(f'\t-> moved to {p}')

        with open(successfull_downloads_fn, 'w' if not os.path.exists(successfull_downloads_fn) else 'a') as outf:
            outf.write(f'{name}:{gb_path[:-3]}\n')
    else:
        with open(incorrect_entries_fn, 'w' if not os.path.exists(incorrect_entries_fn) else 'a') as outf:
            outf.write(f'{gb_path}\n')

        print(f'\t-> failed (written to {incorrect_entries_fn})')


def check_if_already_downloaded(name):
    everything = {}

    if not os.path.exists('successfully_downloaded.txt'):
        with open('successfully_downloaded.txt', 'w') as outf:
            pass

    fn = f'{name.split()[0]}_{SUCCESSFULL_DOWNLOADS_FN}'
    if os.path.exists(fn):
        with open(fn) as inf:
            for entry in inf.readlines():
                splitted = entry.strip().split(':')
                everything[splitted[0]] = splitted[1]

    return name in everything


def download_files(paths, blocksize=33554432):
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


def check_if_already_has_too_few_species():
    with open('too_few_species.txt') as inf:
        genera = [g.strip().split()[0] for g in inf.readlines()]

    if argv[1].capitalize() in genera:
        print(f'Skipping {argv[1].capitalize()}: (known: too few species)')
        exit(0)


def check_if_db_already_exists():
    if argv[1] in cr.list_present_databases(CONF['DATABASE_FOLDER']):
        print(f'{argv[1].capitalize()} database already present. Skipped.')
        exit(0)


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
