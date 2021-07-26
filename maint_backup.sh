
fp="/backups/$(date +"%Y%m%d")_backup"

echo "Creating directory: $fp"
mkdir $fp

echo "Copying jobs folder to $fp/jobs"
cp -r /repo/cagecat/jobs "$fp"

echo "Copying SQL database  to $fp/database.db"
cp /repo/cagecat/database.db "$fp"

echo "Copying Help template to $fp/help.xhtml"
cp /repo/cagecat/templates/help.xhtml "$fp"

echo "Copying logs folder to $fp/process_logs"
cp -r /process_logs "$fp"

echo "Compressing in to $fp.tar.gz"
tar cvf - $fp --remove-files | gzip -9 - > $fp.tar.gz

echo "Finished. Backup available at $1.tar.gz"
