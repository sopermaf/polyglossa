#!/bin/bash          

source /home/sopermaf/.virtualenvs/polyglossa-env/bin/activate
MANAGE_PY="/home/sopermaf/polyglossa/manage.py"

echo "Starting sending emails\n\n"
python $MANAGE_PY send_email_tasks

echo "Starting seminar reminder emails\n\n"
python $MANAGE_PY send_seminar_reminders

echo "Sleeping for $POLYGLOSSA_CRON_SLEEP min(s)"
sleep $POLYGLOSSA_CRON_SLEEP
