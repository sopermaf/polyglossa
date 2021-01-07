#!/bin/bash          

source /home/sopermaf/.virtualenvs/polyglossa-env/bin/activate
MANAGE_PY="/home/sopermaf/polyglossa/manage.py"

echo "Starting sending emails\n\n"
$PYTHON $MANAGE_PY send_emails_tasks

echo "Starting seminar reminder emails\n\n"
$PYTHON $MANAGE_PY send_seminar_reminders

echo "Sleeping for 5 mins"
sleep 5m
