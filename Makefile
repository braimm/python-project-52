install:
	poetry install

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT)

dev:
	poetry run python manage.py runserver

build:
	./build.sh

lint:
	poetry run flake8 task_manager