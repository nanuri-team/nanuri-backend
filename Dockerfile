FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1

ARG ENV_NAME

RUN mkdir /code

COPY ./requirements/* /code/requirements/

WORKDIR /code

RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc python3-dev \
    libpq-dev \
    binutils libproj-dev gdal-bin \
    libsqlite3-mod-spatialite

RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements/$ENV_NAME.txt

COPY . /code

ENTRYPOINT ["/code/scripts/entrypoint.sh"]
