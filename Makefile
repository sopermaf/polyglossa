setup:
	pipenv install --dev

init-hooks:
	pre-commit install

run-hooks:
	pre-commit run --all-files

run-server:
	python manage.py runserver

unit-test:
	pytest
