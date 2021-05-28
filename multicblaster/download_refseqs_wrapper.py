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

        if f == to_download[0]:
            if fn[:-3] in os.listdir(os.path.join(download_base, 'correct')):
                print('\t--> skipped (file already downloaded)')
                break

        time.sleep(0.5)
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
                    if mode == 'w':
                        to_write = f'{name}'
                    else:
                        to_write = f',{name}'
                    outf.write(to_write)
            else:
                # print(f"MD5 checksum not correct: {name}")
                with open(incorrect_entries_fn, 'w' if not os.path.exists(incorrect_entries_fn) else 'a') as outf:
                    outf.write(f'{name}\n')

                print(f'\t--> failed (written to {incorrect_entries_fn})')

def download_batch(seqs):
    total_to_check = len(seqs)
    for count, b in enumerate(seqs, start=1):
        success = 0

        while not success:
            try:

                # if not count % 4:
                #     print('Sending connection ping')
                #     time.sleep(0.34)
                #     ftp.voidcmd('NOOP')

                print(f'({count}/{total_to_check}): {b}')
                # print(b, end='\r')
                path = f"{b}/representative"
                time.sleep(0.5)

                if path in ftp.nlst(b):
                    # print(b, "repr. genome present")
                    time.sleep(0.5)
                    dirs = ftp.nlst(path)
                    if len(dirs) > 1:
                        raise Exception('Multiple assemblies')
                    elif len(dirs) == 1:
                        # new_path = f"{path}/{dirs[0]}"
                        to_download = []
                        # found = 0
                        time.sleep(0.5)
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
                            raise Exception('Incorrect number of files to download')
                        download_files(b, to_download, os.path.join(BASE_DIR, 'Streptomyces'))
                    else:
                        raise Exception('No files?')
                else:
                    print("\t--> skipped (no representative genome found)")

                success = 1
                time.sleep(1.5)
            except EOFError:
                print("Failed to connect")
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
    time.sleep(0.5)
    print('\nLogged in')

    time.sleep(0.5)
    ftp.cwd('genomes/refseq/bacteria')
    print('Changed working directory. Starting..\n')

    return ftp

if __name__ == '__main__':
    init()

    ftp = connect()
    print('Fetching Streptomyces list')
    all_bacteria = ftp.nlst()
    strepto = [c for c in all_bacteria if c.startswith('Streptomyces')]

    time.sleep(0.5)
    ftp.quit()

    BATCHES = (len(strepto) // 50 ) + 1

    for count, entries in enumerate(chunks(strepto, BATCH_SIZE), start=1):
        ftp = connect()
        print(f'Batch {count}/{BATCHES}')

        download_batch(entries)
        ftp.quit()
