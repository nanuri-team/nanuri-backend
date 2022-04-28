FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

RUN mkdir /code

COPY ./requirements/* /code/requirements/

WORKDIR /code

RUN pip install -r requirements/prod.txt

COPY . /code
