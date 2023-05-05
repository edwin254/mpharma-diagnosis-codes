# pull official base image
FROM python:3.9-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN mkdir /app

RUN  pip install --upgrade pip
RUN pip install redis

WORKDIR /app

VOLUME ["/app"]

EXPOSE 6379