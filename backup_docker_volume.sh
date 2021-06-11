docker run -v /multicblaster_storage --name multicblaster_backup ubuntu /bin/bash
docker run --rm --volumes-from multicblaster_backup -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar multicblaster_storage
docker rm multicblaster_backup