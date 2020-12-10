#!/bin/bash          
PYTHON="/home/sopermaf/.virtualenvs/polyglossa-env/bin/python"
MANAGE_PY="/home/sopermaf/polyglossa/manage.py"

echo "Starting sending emails"
$PYTHON $MANAGE_PY send_emails_tasks

echo "Sleeping for 5 mins"
sleep 5m
