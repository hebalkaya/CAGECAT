import ftplib
import hashlib

import bacteria_dump
import time
import os

blocksize = 32*1024*1024
BASE = "ftp.ncbi.nlm.nih.gov"
BASE_DIR = '/lustre/BIF/nobackup/belt017/refseq_gbks'

if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)
os.chdir(BASE_DIR)

ftp = ftplib.FTP(BASE)
# ftp.connect(BASE)

ftp.login()
ftp.cwd('genomes/refseq/bacteria')
# print(ftp.pwd())
def download_files(name, to_download, progression, incorrect_entries_fn='incorrect_entries.txt'):

    print('\t--> downloading')

    for f in to_download:
        time.sleep(0.1)

        fn = f.split('/')[-1]

        with open(fn, 'wb') as outf:
            ftp.retrbinary(f'RETR {f}', outf.write, blocksize=blocksize)

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
                print('\t--> succes')
                # print(f"Succesfully retrieved: {name}")
            else:
                # print(f"MD5 checksum not correct: {name}")
                with open(incorrect_entries_fn, 'w' if not os.path.exists(incorrect_entries_fn) else 'a') as outf:
                    outf.write(f'{name}')

                print(f'\t--> failed (written to {incorrect_entries_fn})')



# below could be in a function
if not os.path.exists('Streptomyces'):
    os.mkdir('Streptomyces')
os.chdir('Streptomyces')

try:
    total_to_check = len(bacteria_dump.strepto)

    for count, b in enumerate(bacteria_dump.strepto, start=1):
        print(f'({count}/{total_to_check}): {b}')
        # print(b, end='\r')
        path = f"{b}/representative"
        if path in ftp.nlst(b):
            # print(b, "repr. genome present")
            dirs = ftp.nlst(path)
            if len(dirs) > 1:
                raise Exception('Multiple assemblies')
            elif len(dirs) == 1:
                # new_path = f"{path}/{dirs[0]}"
                to_download = []
                # found = 0
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
                download_files(b, to_download, (count, total_to_check))
            else:
                raise Exception('No files?')
        else:
            print("\t--> no representative genome found")

        time.sleep(1.5)
        # break
except KeyboardInterrupt:
    ftp.quit()
    exit(0)

ftp.quit()


