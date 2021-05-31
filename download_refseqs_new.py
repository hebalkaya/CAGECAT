import hashlib
import os
import subprocess
import ftplib
import time
from sys import argv

# genus = 'Streptomyces'
# term = f'(((prokaryota[orgn] AND ("representative genome"[refseq category] OR "reference genome"[refseq category])) AND (latest[filter] AND all[filter] NOT anomalous[filter]))) AND {genus}[Organism]'


BASE = 'ftp.ncbi.nlm.nih.gov'


def init():
    genus = argv[1].capitalize()
    output_fn = f'{genus}_ftp_paths.txt'

    print(f'Fetching FTP paths (writing to {output_fn})')
    subprocess.run(['bash', 'get_ftp_paths.sh', genus, output_fn])
    print('\t--> success')

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
        path, genus, species = tuple(line.strip().split())
        key = ' '.join([genus, species])

        paths = (path, f'{path.split("/")[-1]}_genomic{ext}', f'md5checksums.txt')

        if key in all_paths:
            write_error(key, paths, all_paths)
            print('\tContinuing..')

        all_paths[key] = paths

    return all_paths


def create_dir(*args):
    names = os.path.join(*args)
    if not os.path.exists(names):
        os.makedirs(names, exist_ok=True)
        print(f'\t-> created directory {names}')

    return names


def validate_file(gb_path, name, incorrect_entries_fn='incorrect_entries.txt'):
    genus = name.split()[0]

    with open('md5checksums.txt') as inf:
        for line in inf.readlines():
            splitted = line.strip().split()
            if splitted[-1].endswith('genomic.gbff.gz'):
                ori_chksum = splitted[0]
                break

    with open(gb_path, 'rb') as inf:
        calc_chksum = hashlib.md5(inf.read()).hexdigest()

    if calc_chksum == ori_chksum:
        print('\t-> validated')

        subprocess.run(['gzip', '-d', gb_path])
        print('\t-> unzipped')

        p = create_dir(genus, 'validated')

        os.rename(gb_path[:-3], os.path.join(p, gb_path[:-3]))
        print(f'\t-> moved to {p}')
    else:
        with open(incorrect_entries_fn, 'w' if not os.path.exists(incorrect_entries_fn) else 'a') as outf:
            outf.write(f'{gb_path}\n')

        print(f'\t--> failed (written to {incorrect_entries_fn})')


def postpone_request(t):
    time.sleep(0.34 - (t))


def download_files(paths, blocksize=33554432):
    total = len(paths)
    for count, (key, value) in enumerate(paths.items(), start=1):
        print(f'({count}/{total}): {key}')
        base, gb_path, md5_path = value
        ftp = ftplib.FTP(BASE)

        t = time.time()
        ftp.login()

        postpone_request(t)
        ftp.cwd('/'.join(base[5:].split('/')[2:]))

        for counter, f in enumerate((gb_path, md5_path), start=1):
            print(f'\t-> downloading ({counter}/{2})')
            time.sleep(0.34)
            with open(f, 'wb') as outf:
                ftp.retrbinary(f'RETR {f}', outf.write, blocksize=blocksize)

        validate_file(gb_path, key)


def chunks(seqs, batch_size):
    for i in range(0, len(seqs), batch_size):
        yield seqs[i:i+batch_size]

if __name__ == '__main__':
    fn = init()

    paths = parse_paths(fn)
    download_files(paths)
