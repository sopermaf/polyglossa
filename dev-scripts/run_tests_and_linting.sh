set -e

echo "Running Django Tests"
pipenv run pytest

echo "Running Python Linting"
pipenv run pylint -d fixme payments polyglossa class_bookings learning_materials

echo "Running Frontend Linting"
cd frontend/
npm run lint
