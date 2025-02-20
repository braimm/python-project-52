install:
	poetry install

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

dev:
	poetry run python manage.py runserver

build:
	./build.sh

migrate:
	poetry run python manage.py migrate

lint:
	poetry run flake8 task_manager

test:
	poetry run python manage.py test

translate:
	poetry run python manage.py makemessages -l ru

compile_translate:
	poetry run python manage.py compilemessages --ignore=.venv

test-coverage-report:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage xml -o coverage.xml

coverage:
	poetry run coverage report
