set -e

pipenv run python manage.py test

pipenv run pylint -d fixme payments polyglossa class_bookings

cd frontend/
npm run lint