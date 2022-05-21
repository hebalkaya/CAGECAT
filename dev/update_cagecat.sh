#!/bin/bash
# Author: Matthias van den Belt

container_name=$1 # intentionally left out for safety reasons

echo "--> Copying jobs folder and database.db to host"
docker cp "$container_name":/repo/cagecat/database.db database.db
#docker cp "$container_name":/repo/cagecat/jobs jobs

echo "--> Cloning new repo"
git clone https://github.com/malanjary-wur/CAGECAT.git && \
mv CAGECAT/ repo

echo "--> Stopping container $container_name"
docker container stop $container_name

echo "--> Copying files from host to container"
# as there is no /repo/cagecat/database.db and
# no /repo/cagecat/jobs on the git repo, these are unaffected.
# Nevertheless, we created a backup of them earlier
docker cp repo "$container_name":/

echo "--> Starting container $container_name"
docker container start $container_name

echo "Restarting uwsgi"
docker exec "$container_name" uwsgi --reload /tmp/uwsgi-master.pid

echo " -> Old files of files that had their name CHANGED are still present"

echo "Done!"
