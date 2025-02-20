### Tests and linter status:
[![Actions Status](https://github.com/braimm/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/braimm/python-project-52/actions)
[![Github Actions Status](https://github.com/braimm/python-project-52/workflows/Python%20CI/badge.svg)](https://github.com/braimm/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/305890f442c11e7f44ff/maintainability)](https://codeclimate.com/github/braimm/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/305890f442c11e7f44ff/test_coverage)](https://codeclimate.com/github/braimm/python-project-52/test_coverage)


## Description of project

**Task manager** - web-application based on the Django framework that allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.

## How to use
1. Register on the website.
2. Create your own **labels** and **statuses** for tasks.
3. Create your **tasks**, **task descriptions**, assign **statuses**, **labels** and **executor**.

**Link to demonstrate how the project works:** https://python-project-52-szrx.onrender.com/


![Main Page](https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6ImZiZDIzODJhMTkwNWU1YTQ0Y2I5MTY5MTIzMjBjZjVmLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=319cd6d58a8b270c0a74584e988920e2d1bd4ee92498472e107337f9bff7c810)
![New User Registration Page](https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6IjI4MDM3ODZhNDg1YzFhNmI1MWExYjgxODkwNTU5MDI3LnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=c5f5d99f1788e52d6b95b9c31a9305a63684f1071d14b46f9442b30f47addd17)
![Task List View Page](https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6ImY1MWQ2NDVlZDhmNzAyZTdlYmUxMmJlNzUyMWIzYWNiLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=53760b90a99c39fe9e6fa9f419fe4ae4f7606407adf8027ebb81b7b6d8c17965)



## How to install and start code project
### Required for installation amd start:
1. Python (version or newer)
2. pip (version 23.3.1 or newer)
3. Poetry (version 1.7.1 or newer)
1. Configured DBMS (PostgreSQL, SQlite or other)
2. Set environment variable: DATABASE_URL and SECRET_KEY

### Installation steps:
1. Install Poetry
```bash
pip install poetry
```
2. Copy project from repository, manually or with the command
```bash
git clone git@github.com:braimm/python-project-52.git
```
3. Run inside the project's directory the following command to install dependencies and migration
```bash
make build
```
4. Start server web-application
```bash
make start
```