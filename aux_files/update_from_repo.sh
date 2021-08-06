#!/bin/bash
# Author: Matthias van den Belt

echo "--> Copying jobs folder and database.db to host"
docker cp cagecat_service:/repo/cagecat/database.db database.db
docker cp cagecat_service:/repo/cagecat/jobs jobs

echo "--> Cloning new repo"
git clone git@git.wur.nl:belt017/thesis_repo.git && \
mv thesis_repo/ repo

echo "--> Copying files from host to container"
# as there is no /repo/cagecat/database.db and
# no /repo/cagecat/jobs on the git repo, these are unaffected.
# Nevertheless, we created a backup of them earlier
docker cp repo cagecat_service:/

echo "Restarting uwsgi"
docker exec cagecat_service uwsgi --reload /tmp/uwsgi-master.pid

echo "Done!"
