import ftplib
import bacteria_dump
import time

BASE = "ftp.ncbi.nlm.nih.gov"

ftp = ftplib.FTP(BASE)
# ftp.connect(BASE)

ftp.login()
ftp.cwd('genomes/refseq/bacteria')
# print(ftp.pwd())
def download_files(to_download):
    for f in to_download:
        fn = f.split('/')[-1]
        with open(fn, 'wb') as outf:
            ftp.retrbinary(f'RETR {f}', outf.write)
            print('Written file:', fn)

            # TODO: check md5 checksums
    pass


for b in bacteria_dump.strepto:
    print("Checking", b)
    path = f"{b}/representative"
    if path in ftp.nlst(b):
        print(b, "repr. genome present")
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
            print('The files to be downloaded are:', to_download)
            download_files(to_download)

            if len(to_download) in (0, 1):
                raise Exception('Incorrect number of files to download')

        else:
            raise Exception('No files?')


    else:
        print("No repr. genome for", b)
    time.sleep(1.5)
    # break

ftp.quit()


