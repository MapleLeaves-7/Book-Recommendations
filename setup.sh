#!/usr/bin/env bash

docker exec -i book-recommendations_db_1 psql -U user books < postgres_backup.sql

python -m venv setup_venv
source setup_venv/bin/activate

python -m pip install -r search/requirements.txt
python search/index_data.py

deactivate