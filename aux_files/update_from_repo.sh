# Author: Matthias van den Belt

echo "--> Backing up old files"
#TODO: would: add folder of date and move cp files to there
docker cp cagecat_service:/repo/cagecat/database.db database.db
docker cp cagecat_service:/repo/cagecat/jobs jobs

echo "--> Removing old repo"
rm -rf repo

echo "--> Cloning new repo"
git clone git@git.wur.nl:belt017/thesis_repo.git && \
mv thesis_repo/ repo

echo "--> Copying files from host to container"
# as there is no /repo/cagecat/database.db and
# no /repo/cagecat/jobs on the git repo, these are unaffected.
# Nevertheless, we created a backup of them earlier
docker cp repo cagecat_service:/

echo "--> Validate manually that the release number has changed"
docker exec cagecat_service cat /repo/cagecat/templates/help.xhtml

echo "Restarting uwsgi"
docker exec cagecat_service uwsgi --reload /tmp/uwsgi-master.pid

echo "Done!"
