# Author: Matthias van den Belt

echo "--> Backing up old files"
#TODO: add folder of date and move cp files to there
docker cp multicblaster_trial:/repo/multicblaster/database.db database.db
docker cp multicblaster_trial:/repo/multicblaster/jobs jobs

echo "--> Removing old repo"
rm -rf repo

echo "--> Cloning new repo"
git clone git@git.wur.nl:belt017/thesis_repo.git && \
mv thesis_repo/ repo

echo "--> Copying files from host to container"
# as there is no /repo/multicblaster/database.db and
# no /repo/multicblaster/jobs on the git repo, these are unaffected.
# Nevertheless, we created a backup of them earlier
docker cp repo multicblaster_trial:/

echo "--> Validate manually that the release number has changed"
docker exec multicblaster_trial cat /repo/multicblaster/templates/help.xhtml

echo "--> You are not done yet. Command to execute:"
echo "    --> docker exec multicblaster_trial ps aux | grep uwsgi"
echo "--> Find the uwsgi master process (process with the outlying pid (mostly 14))"
echo "--> Execute the following command"
echo "    --> docker exec multicblaster_trial kill <pid>"
echo "--> The uwsgi process will be restarted by supervisor and you are done."



