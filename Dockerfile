FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1

ARG ENV_NAME

RUN mkdir /code

COPY ./requirements/* /code/requirements/

WORKDIR /code

RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    apt-get install -y libpq-dev

RUN pip install -r requirements/$ENV_NAME.txt

COPY . /code
