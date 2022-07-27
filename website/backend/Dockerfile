FROM python:3.9-slim

WORKDIR /usr/src/app

# Download psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./website/backend .

# ENTRYPOINT [ "python", "books_api.py" ]