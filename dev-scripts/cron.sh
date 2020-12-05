#!/bin/bash          
PYTHON_VENV="/home/sopermaf/.virtualenvs/polyglossa-env/bin/python"
MANAGE="/home/sopermaf/polyglossa/manage.py"

echo "Starting sending emails"
$PYTHON_VENV $MANAGE send_emails

echo "Sleeping for 5 mins"
sleep 5m
