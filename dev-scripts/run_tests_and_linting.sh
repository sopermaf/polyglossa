#!/bin/bash
set -e

echo "Running Django Tests"
pipenv run pytest class_bookings/ payments/ learning_materials/ tasks/

echo "Running Python Linting"
pipenv run pylint -d fixme payments polyglossa class_bookings learning_materials tasks

echo "Running Frontend Linting"
cd frontend/
npm run lint
