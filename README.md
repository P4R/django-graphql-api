# DJANGO GRAPHQL API Z1

## Deploy server
---
- Docker Compose is required (https://docs.docker.com/compose/install/)

Clone Repo:
```bash
git clone https://github.com/P4R/django-graphql-api-z1
```

Move to project folder:
```bash
cd django-graphql-api-z1
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

## TASKS

- [X] Un usuario puede registrarse introduciendo su email y eligiendo un nombre de usuario libre y una contraseña
- [X] Un usuario debe ser capaz de logarse utilizando email y contraseña.
- [X] Un usuario debe poder cambiar su contraseña.
- [X] Un usuario debe poder restaurar su contraseña recibiendo un email con un magic link.
- [X] Un usuario puede publicar una idea como un texto corto en cualquier momento.
- [X] Un usuario puede establecer la visibilidad de una idea: publica (todos pueden verla), protegida (solo otros usuarios que siguen al usuario de la idea pueden verla) y privada (solo el usuario que creó la idea puede verla)
- [X] Un usuario puede establecer la visibilidad de una idea en el momento de su creacion o editarla posteriormente.
- [X] Un usuario puede consultar todas las ideas que ha publicado ordenadas de mas recientes a mas antiguas.
- [X] Un usuario puede borrar una idea publicada.
- [X] Un usuario puede solicitar seguir a otro usuario
- [X] Un usuario puede ver el listado de solicitudes de seguimiento recibidas y aprovarlas o denegarlas
- [X] Un usuario puede ver el listado de gente a la que sigue
- [X] Un usuario puede ver el listado de gente que le sigue
- [X] Un usuario puede dejar de seguir a alguien
- [X] Un usuario puede eliminar a otro usuario de su lista de seguidores
- [X] Un usuario puede realizar una busqueda de otros usuarios introduciendo un nombre de usuario o parte de uno
- [X] Un usuario puede ver la lista de ideas de cualquier otro usuario, teniendo en cuenta la visibilidad de cada idea.
- [X] Un usuario puede ver un timeline de ideas compuesto por sus propias ideas y las ideas de los usuarios a los que sigue, teniendo en cuenta la visibilidad de cada idea.

## TODO

- [ ] Un usuario debe recibir una notificación cada vez que un usuario al que sigue publica una idea nueva a la que tiene acceso.

  Habria que registrar los tokens de los dispositivos en el usuario para enviarles las notificaciones utilizando firebase

## TO IMPROVE

- [ ] Añadir paginación a las queries.