FROM python:3.8-slim-buster

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential

RUN mkdir /code

COPY ./requirements/* /code/requirements/

WORKDIR /code

RUN pip install -r requirements/prod.txt

COPY . /code
