FROM python:3.9.6-buster

ENV PYTHONUNBUFFERED=1

ARG DJANGO_UID=1000
ARG DJANGO_GID=1000

RUN set -ex \
    && groupadd -o -g "${DJANGO_GID}" django \
    && useradd -o -u "${DJANGO_UID}" -g "${DJANGO_GID}" \
    -m -s /bin/bash django


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh /home/django
RUN chmod +x /home/django/entrypoint.sh
USER django

EXPOSE 8000/tcp

ENTRYPOINT ["/home/django/entrypoint.sh"]