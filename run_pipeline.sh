set -e

echo "Running Django Tests"
pipenv run python manage.py test

echo "Running Python Linting"
pipenv run pylint -d fixme payments polyglossa class_bookings

echo "Running Frontend Linting"
cd frontend/
npm run lint
