# TODO: remove as this is only for development

import subprocess

def main():
    cmds = [
        'docker cp repo cagecat_dev:/',
        'docker exec cagecat_dev uwsgi --reload /tmp/uwsgi-master.pid'
    ]

    for c in cmds:
        subprocess.check_output(c.split())

    print('Success!')

if __name__ == '__main__':
    main()
