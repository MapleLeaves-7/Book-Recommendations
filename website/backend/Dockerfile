FROM python:3.9

WORKDIR /usr/src/app

# Download psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# copy and download python package requirements
COPY ./website/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# copy main code
COPY ./website/backend .

RUN mkdir -p db
# copy sqlalchemy model
COPY ./db/models.py ./db/
# copy config for postgres docker image that will be run
COPY ./website/backend/db_config.py ./db/