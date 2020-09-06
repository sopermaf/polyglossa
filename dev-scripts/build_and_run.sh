#!/bin/bash
cd frontend/
npm run build

cd ..
python manage.py runserver
