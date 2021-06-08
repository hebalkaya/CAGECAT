import subprocess
import time
import os
from download_refseqs import BASE_DIR, COMPLETE_DOWNLOADS_FILE
from config import CONF

SLEEPING_TIME = 60
CPUS = "10"
BATCH_SIZE = "30"

def init():
    if not os.path.exists(CONF['DATABASE_FOLDER']):
        os.makedirs(CONF['DATABASE_FOLDER'], exist_ok=True)

    os.chdir(CONF['DATABASE_FOLDER'])

    if not os.path.exists('logs'):
        os.mkdir('logs')

def read_contents():
    with open(COMPLETE_DOWNLOADS_FILE) as inf:
        to_create = [line.strip() for line in  inf.readlines()]

    return to_create


def list_files(genus):
    for root, dir, files in os.walk(os.path.join(BASE_DIR, genus, 'validated')):
        all_files = [os.path.join(root, f) for f in files]
    # print(all_files)
    return all_files


def main():
    init()

    try:
        while True:
            to_create = read_contents()

            if not to_create:
                print(f'No database to create. Waiting {SLEEPING_TIME} seconds')
                time.sleep(SLEEPING_TIME)
            else:
                for genus in to_create:
                    print(f'Creating {genus} database')

                    # res = subprocess.run(['echo', 'hello'], capture_output=True)
                    cmd = ["cblaster", "makedb", "--name", genus,
                           "--cpus",  CPUS, "--batch", BATCH_SIZE,
                           "--force"]
                    cmd.extend(list_files(genus))

                    with open(os.path.join('logs', f'{genus}_creation.log'), 'w') as outf:
                        res = subprocess.run(cmd, stderr=outf, stdout=outf, text=True)
                    # print(res.stdout)

                    if res.returncode != 0:
                        print('Something went wront. Exiting..')
                        exit(1)

                to_do = []
                for g in read_contents():
                    if g not in to_create:
                        to_do.append(g)

                with open(COMPLETE_DOWNLOADS_FILE, 'w') as outf:
                    for genus in to_do:
                        outf.write(f'{genus}\n')
    except KeyboardInterrupt:
        print('Exiting...')

main()
