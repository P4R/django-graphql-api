# DJANGO GRAPHQL API
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
## Deploy server

- Docker Compose is required (https://docs.docker.com/compose/install/)

Clone Repo:
```bash
git clone https://github.com/P4R/django-graphql-api
```

Move to project folder:
```bash
cd django-graphql-api
```

Start server:
```bash
 docker-compose up -d
```

Stop server:
```bash
 docker-compose stop
```

## Run tests

Note: 
- Tests with **slqlite** for run it in app container
- Execute command in root project folder


```bash
docker-compose run --rm app python manage.py test api.tests --settings=app.settings_test
```

## Django admin panel
http://127.0.0.1:8000/admin

## API
http://127.0.0.1:8000/api/graphql
