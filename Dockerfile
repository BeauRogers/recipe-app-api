FROM python:3.7-alpine
MAINTAINER Beau Personal Project

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client

# install temporary packages that are needed to instal, but aren't needed later
# --virtual creates aliase for dependancies such that we can remove easier later
RUN apk add --update --no-cache --virtual .temp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r ./requirements.txt
# Now we will delete the tempoaray 'virtual' package
RUN apk del .temp-build-deps


RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
