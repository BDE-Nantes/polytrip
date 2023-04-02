# syntax=docker/dockerfile:1
FROM python:3.9-buster AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        build-essential \
        zlib1g-dev \
        libxmlsec1-openssl

WORKDIR /app

COPY ./requirements /app/requirements
RUN pip install pip -U setuptools wheel
RUN pip install -r requirements/base.txt

COPY ./src /app/src


FROM node:14-alpine AS frontend-build

WORKDIR /app

COPY ./polytrip-front /app/front-public

WORKDIR /app/front-public

RUN npm ci

RUN npm run build

WORKDIR /app

COPY ./polytrip-admin-front /app/front-admin

WORKDIR /app/front-admin

RUN npm ci

RUN npm run build

WORKDIR /app

COPY /app/front-admin/dist /app/src/templates/front-admin
COPY /app/front-public/dist /app/src/templates/front-public
