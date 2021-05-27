import ftplib
import hashlib

import bacteria_dump
import time
import os
import subprocess

blocksize = 32*1024*1024
BASE = "ftp.ncbi.nlm.nih.gov"
BASE_DIR = '/lustre/BIF/nobackup/belt017/refseq_gbks'

if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)

os.chdir(BASE_DIR)

ftp = ftplib.FTP(BASE)
# ftp.connect(BASE)

def connect():
    time.sleep(0.34)
    ftp.login()

    time.sleep(0.34)
    ftp.cwd('genomes/refseq/bacteria')

connect()
# print(ftp.pwd())
def download_files(name, to_download, download_base, incorrect_entries_fn='incorrect_entries.txt', errors_fn='error_entries.txt'):

    print('\t--> downloading')

    for f in to_download:
        fn = f.split('/')[-1]

        time.sleep(0.34)
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

            else:
                # print(f"MD5 checksum not correct: {name}")
                with open(incorrect_entries_fn, 'w' if not os.path.exists(incorrect_entries_fn) else 'a') as outf:
                    outf.write(f'{name}\n')

                print(f'\t--> failed (written to {incorrect_entries_fn})')

# below could be in a function
if not os.path.exists('Streptomyces'):
    os.mkdir('Streptomyces')

if not os.path.exists('Streptomyces/correct'):
    os.mkdir('Streptomyces/correct')
os.chdir('Streptomyces')

try:
    # checker = ['Streptomyces_decoyicus', 'Streptomyces_durhamensis']
    total_to_check = len(bacteria_dump.strepto)

    for count, b in enumerate(bacteria_dump.strepto, start=1):
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
                time.sleep(0.34)
                if path in ftp.nlst(b):
                    # print(b, "repr. genome present")
                    time.sleep(0.34)
                    dirs = ftp.nlst(path)
                    if len(dirs) > 1:
                        raise Exception('Multiple assemblies')
                    elif len(dirs) == 1:
                        # new_path = f"{path}/{dirs[0]}"
                        to_download = []
                        # found = 0
                        time.sleep(0.34)
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
                time.sleep(0.9)
            except EOFError:
                print("Failed to connect")
                # connect()
        # breaks
except KeyboardInterrupt:
    time.sleep(0.34)
    ftp.quit()
    exit(0)

time.sleep(0.34)
ftp.quit()


