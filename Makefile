install:
	poetry install

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

dev:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate

lint:
	poetry run flake8 task_manager

translate:
	poetry run python manage.py makemessages -l ru

compile-translate:
	poetry run python manage.py compilemessages --ignore=.venv

test:
	poetry run python3 manage.py test

check-coverage:
	poetry run coverage run --source='.' manage.py test

coverage-report:
	poetry run coverage xml -o coverage.xml

coverage-view:
	poetry run coverage report
