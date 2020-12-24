#!/bin/bash
set -e

echo "Pulling from Git Master"
git pull

echo "Collecting static files"
python manage.py collectstatic

echo "Syncing db changes"
python manage.py makemigrations
python manage.py migrate --run-syncdb

echo "Reloading Webapp with changes"
touch /var/www/www_polyglossa_com_wsgi.py