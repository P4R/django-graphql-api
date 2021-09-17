# DJANGO GRAPHQL API

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
