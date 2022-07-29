FROM python:3.9-slim

WORKDIR /usr/src/app

# Download psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY ./website/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./website/backend .

RUN mkdir -p db
# sqlalchemy model
COPY ./db/models.py ./db/
# config for postgres docker image that will be run
COPY ./website/backend/db_config.py ./db/

# ENTRYPOINT [ "python", "books_api.py" ]