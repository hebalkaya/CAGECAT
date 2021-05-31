import hashlib
import subprocess

import time
import os
import ftplib

blocksize = 32*1024*1024
BASE = "ftp.ncbi.nlm.nih.gov"
BASE_DIR = '/lustre/BIF/nobackup/belt017/refseq_gbks'


BATCH_SIZE = 50


def chunks(seqs, batch_size):
    for i in range(0, len(seqs), batch_size):
        yield seqs[i:i+batch_size]

def download_files(name, to_download, download_base, incorrect_entries_fn='incorrect_entries.txt', errors_fn='error_entries.txt'):

    print('\t--> downloading')

    for f in to_download:
        fn = f.split('/')[-1]

        time.sleep(0.35)
        # try:
        with open(fn, 'wb') as outf:
            ftp.retrbinary(f'RETR {f}', outf.write, blocksize=blocksize)
        # except EOFError:
        #     print(f'\t--> error (written to {errors_fn}')
        # with open(errors_fn, 'w' if not os.path.exists(errors_fn) else 'a') as outf:
        # outf.write(f'{name}\n')
        # break

        if f == to_download[-1]: # indicates checksums
            print('\t--> checking MD5 checksum')
            # get the checksum to validate file
            with open(fn) as inf:
                for line in inf.readlines():
                    splitted = line.strip().split()
                    if splitted[-1].endswith('genomic.gbff.gz'):
                        ori_chksum = splitted[0]
                        break

            with open(to_download[0].split('/')[-1], 'rb') as inf:
                calc_chksum = hashlib.md5(inf.read()).hexdigest()

            if calc_chksum == ori_chksum:

                print('\t--> success')
                # print(f"Succesfully retrieved: {name}")
                actual_fn = to_download[0].split('/')[-1]
                subprocess.run(['gzip', '-d', actual_fn])
                os.rename(os.path.join(download_base, actual_fn[:-3]), os.path.join(download_base, 'correct', actual_fn[:-3]))
                print('\t--> extracted and moved')

                successfull_fn = 'successfully_downloaded.txt'

                mode = 'w' if not os.path.exists(successfull_fn) else 'a'
                with open(successfull_fn, mode) as outf:
                    assembly_id = to_download[0].split('/')[-1][:-3]
                    to_write = f'{name}:{assembly_id}\n'
                    outf.write(to_write)
            else:
                # print(f"MD5 checksum not correct: {name}")
                with open(incorrect_entries_fn, 'w' if not os.path.exists(incorrect_entries_fn) else 'a') as outf:
                    outf.write(f'{name}\n')

                print(f'\t--> failed (written to {incorrect_entries_fn})')

def check_if_already_downloaded(name):
    everything = {}

    if not os.path.exists('successfully_downloaded.txt'):
        with open('successfully_downloaded.txt', 'w') as outf:
            pass

    with open('successfully_downloaded.txt') as inf:
        for entry in inf.readlines():
            splitted = entry.strip().split(':')
            everything[splitted[0]] = splitted[1]

    return name in everything


def download_batch(seqs, error_fn='errors.txt'):

    total_to_check = len(seqs)
    for count, b in enumerate(seqs, start=1):
        success = 0
        print(f'({count}/{total_to_check}): {b}')

        if check_if_already_downloaded(b):
            print('\t--> skipped (file already downloaded)')
            continue

        while not success:
            try:

                # if not count % 4:
                #     print('Sending connection ping')
                #     time.sleep(0.34)
                #     ftp.voidcmd('NOOP')
                # print(b, end='\r')
                path = f"{b}/representative"

                time.sleep(0.35)
                if path in ftp.nlst(b):
                    # print(b, "repr. genome present")
                    time.sleep(0.35)
                    dirs = ftp.nlst(path)
                    if len(dirs) > 1:
                        print(f'ERROR: multiple assemblies (written to {error_fn})')
                        with open(error_fn, 'w' if not os.path.exists(error_fn) else 'a') as outf:
                            outf.write(f'{b},multiple assemblies')
                        break
                        # raise Exception('Multiple assemblies')
                    elif len(dirs) == 1:
                        # new_path = f"{path}/{dirs[0]}"
                        to_download = []
                        # found = 0
                        time.sleep(0.35)
                        for file in ftp.nlst(dirs[0]):
                            if file.endswith('genomic.gbff.gz'):
                                # print('We should download:', file)
                                # found = 1
                                to_download.append(file)
                            # print(file)
                            if file.endswith('md5checksums.txt'): # do it in the loop to check if the file exists to prevent future errors when for some reason the file doesnt xist
                                to_download.append(file)
                        # print('The files to be downloaded are:', to_download)

                        if len(to_download) in (0, 1, 3, 4):
                            print(f'ERROR: incorrect number of files to download (written to {error_fn})')
                            with open(error_fn, 'w' if not os.path.exists(error_fn) else 'a') as outf:
                                outf.write(f'{b},incorrect file number')
                            break
                            # raise Exception('Incorrect number of files to download')
                        download_files(b, to_download, os.path.join(BASE_DIR, 'Streptomyces'))
                    else:
                        print(f'ERROR: no files found (written to {error_fn})')
                        with open(error_fn, 'w' if not os.path.exists(error_fn) else 'a') as outf:
                            outf.write(f'{b},no files found')
                        break
                else:
                    print("\t--> skipped (no representative genome found)")

                success = 1
                time.sleep(1.5)
            except EOFError:
                print("Failed to connect. Waiting one minute before reconnecting")
                time.sleep(60)
                # connect()

def init():
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)

    os.chdir(BASE_DIR)

    if not os.path.exists('Streptomyces'):
        os.mkdir('Streptomyces')

    if not os.path.exists('Streptomyces/correct'):
        os.mkdir('Streptomyces/correct')

    os.chdir('Streptomyces')


def connect():
    ftp = ftplib.FTP(BASE, user='anonymous', passwd='password')

    ftp.login()
    time.sleep(0.35)
    print('\nLogged in')

    time.sleep(0.35)
    ftp.cwd('genomes/refseq/bacteria')
    print('Changed working directory. Starting..\n')

    return ftp

if __name__ == '__main__':
    init()

    ftp = connect()

    print("Fetching all bacteria..")
    all_bacteria = ftp.nlst()

    print('Getting al genuses..')
    all_genus = []
    for b in all_bacteria:
        genus = b.split('_')[0]
        if genus not in all_genus:
            all_genus.append(genus)

    print(f'Total number of genuses: {len(all_genus)}')

    # TODO: here we could loop over the genuses

    print(f'Filtering for: Streptomyces')
    strepto = [c for c in all_bacteria if c.startswith('Streptomyces')]

    time.sleep(0.35)
    ftp.quit()

    BATCHES = (len(strepto) // 50 ) + 1
    print(f"In total, {len(strepto)} are genomes are going to be downloaded")

    for count, entries in enumerate(chunks(strepto, BATCH_SIZE), start=1):
        ftp = connect()
        print(f'Batch {count}/{BATCHES}')

        download_batch(entries)
        ftp.quit()
