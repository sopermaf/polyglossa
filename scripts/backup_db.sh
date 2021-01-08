#!/bin/bash
set -e

timestamp=`date +%Y-%m-%d`

# relative to home dir
db_backup_file="db-backup_$timestamp.sql"

cd
mysqldump -u sopermaf -h sopermaf.mysql.pythonanywhere-services.com --set-gtid-purged=OFF 'sopermaf$polyglossa'  > $db_backup_file
