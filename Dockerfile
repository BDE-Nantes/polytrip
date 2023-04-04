# syntax=docker/dockerfile:1
# Stage 1: build backend requirements
FROM python:3.9-buster AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        build-essential \
        zlib1g-dev

WORKDIR /app

COPY ./requirements /app/requirements
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pip -U setuptools wheel \
        && pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements/base.txt

# Stage 2: build frontends requirements
FROM node:14-alpine AS frontend-build

WORKDIR /app

COPY ./polytrip-front /app/front-public

WORKDIR /app/front-public

RUN npm config set strict-ssl false

RUN npm ci

RUN npm run build

WORKDIR /app

COPY ./polytrip-admin-front /app/front-admin

WORKDIR /app/front-admin

RUN npm ci

RUN npm run build

# Stage 3: build Docker image
FROM python:3.9-buster AS production

RUN apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client \
        libgdal20 \
        libgeos-c1v5 \
        libproj13

COPY --from=build /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY --from=build /usr/local/bin/uwsgi /usr/local/bin/uwsgi

WORKDIR /app
COPY ./bin/docker_start.sh /start.sh
RUN mkdir /app/log /app/config

COPY ./src /app/src
COPY --from=frontend-build /app/front-admin/dist /app/src/polytrip/templates/front-admin
COPY --from=frontend-build /app/front-public/dist /app/src/polytrip/templates/front-public

RUN useradd -M -u 1000 user
RUN chown -R user /app

USER user

ENV DJANGO_SETTINGS_MODULE=polytrip.conf.docker

ARG SECRET_KEY=dummy

RUN python src/manage.py collectstatic --noinput

EXPOSE 8000
CMD ["/start.sh"]
