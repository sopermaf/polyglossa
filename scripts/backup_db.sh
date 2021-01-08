#!/bin/bash
# no fail on error flag in case of failure to remove files 

timestamp=`date +%Y-%m-%d`

# relative to home dir
db_backup_file="db-backup_$timestamp.sql"

cd

# remove all but the 3 most recent backups
ls -tp db-backup_*.txt | tail -n +4 | tr '\n' '\0' | xargs -0 rm --

mysqldump -u sopermaf -h sopermaf.mysql.pythonanywhere-services.com --set-gtid-purged=OFF 'sopermaf$polyglossa'  > $db_backup_file
