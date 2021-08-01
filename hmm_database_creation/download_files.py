import subprocess
from sys import argv
import os
import ftplib
import time
import hashlib
import sys

sys.path.append('..')
from config_files.config import *

def parse_paths(fp, ext='.gbff.gz'):
    genus_paths = {}

    with open(fp) as inf:
        all_lines = inf.readlines()

    for line in all_lines:
        # line looks like this:
        # ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/495/915/GCF_000495915.1_PseChl   Pseudomonas chloritidismutans
        splitted = line.strip().split()
        ftp_path, genus, species = splitted[0].replace(BASE_URL, ''), splitted[1], ' '.join(splitted[2:])
        key = ' '.join([genus, species])

        assembly_name = ftp_path.split('/')[-1]
        base_dir = ('/'.join(ftp_path[6:].split('/')[:-1]) + f'/{assembly_name}/')
        # [6:] get rid of ftp://. Rejoin with forward slashes, leave out
        # file name and add trailing forward flash.
        # example outcome: ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/495/915/

        genome_file_path = base_dir + assembly_name + '_genomic' + ext
        # [-1]: get file name of assembly

        md5_file_path = base_dir + 'md5checksums.txt'

        if key in genus_paths:  # sometimes NCBI has double genus entries.
            # to make sure we download everything, we just save it under
            # a different name
            key += '1'

        genus_paths[key] = (genome_file_path, md5_file_path)

    print('     -> FTP paths parsed')
    return genus_paths


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
        print(f'     -> created directory: {names}')

    return names


def validate_download(gb_path):
    print('         -> validation.. ', end='\r')

    with open(os.path.join(BASE_DIR, 'md5checksums.txt')) as inf:
        for line in inf.readlines():
            splitted = line.strip().split()
            if splitted[-1].endswith('genomic.gbff.gz'):
                ori_chksum = splitted[0]
                break

    with open(gb_path, 'rb') as inf:
        calc_chksum = hashlib.md5(inf.read()).hexdigest()

    if calc_chksum == ori_chksum:
        print('         -> validation --> ok')
    else:
        print('         -> validation --> incorrect')
        return False
        # check manually (or create script to grep the log files of cron job
        # with this line)

    subprocess.run(['gzip', '-d', gb_path])
    print('         -> unzipped')

    return True


def download_files(genus, paths, output_dir, blocksize=33554432):
    # TODO: check if checksum has changed

    present_files = os.listdir(output_dir)
    species_count = len(paths)

    for count, (species, paths) in enumerate(paths.items(), start=1):
        print(f'     -> {count}/{species_count}: {species}')
        # paths[0] looks like:
        # ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/820/515/GCF_000820515.1_ASM82051v1/GCF_000820515.1_ASM82051v1_genomic.gbff.gz
        genome_file_name = paths[0].split('/')[-1]
        if genome_file_name[:-3] in present_files:
            print(f'         -> already present: {genome_file_name[:-3]}')
        else:
            for i, fp in enumerate(paths, start=1):
                ftp = ftplib.FTP(BASE_URL)

                print(f'         -> downloading file {i} of 2')
                file_name = fp.split('/')[-1]
                ftp.login()
                time.sleep(0.34)

                with open(os.path.join(BASE_DIR, file_name), 'wb') as outf: # now with .gz as we download it as compressed
                    ftp.retrbinary(f'RETR {fp}', outf.write, blocksize=blocksize)
                time.sleep(0.34)

            genome_file_path = os.path.join(BASE_DIR, genome_file_name)
            if validate_download(genome_file_path):
                os.rename(genome_file_path[:-3], os.path.join(BASE_DIR, genus,
                                                         genome_file_path.split('/')[-1][:-3]))
                # [:-3] is to remove .gz
                print(f'         -> moved to {genus} folder')


if __name__ == '__main__':
    if argv[1] == 'everything_has_been_downloaded':
        subprocess.run(['touch', os.path.join(BASE_DIR, 'databases_to_create', 'stop_creating_databases')])
        exit(0)

    genus = argv[1].split('_')[0]

    paths = parse_paths(argv[1])
    if len(paths) < THRESHOLDS['representative_genomes_number']:
        print(f'  skipping {genus} ({len(paths)} < {THRESHOLDS["representative_genomes_number"]})')

        mode = 'a' if os.path.exists('too_few_species.txt') else 'w'
        with open('too_few_species.txt', mode) as outf:  # gets overwritten every time
            for species, file_paths in paths.items():
                outf.write(f'{species},{file_paths[0]},{file_paths[1]}\n')
                # species,genome file ftp path, md5 checksum ftp path
        exit(0)

    output_dir = create_dir(BASE_DIR, genus)
    download_files(genus, paths, output_dir)

    # TODO: add somewhere which db's are ready to be created. Or immedidtealy create the db?
    create_dir(BASE_DIR, 'databases_to_create')
    subprocess.run(['touch', os.path.join(BASE_DIR, 'databases_to_create', genus)])
