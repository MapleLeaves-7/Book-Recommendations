"""
Database configuration for postgres docker image.
File will be used when website backend docker image is run, and postgres docker image is run concurrently.
"""

import logging

try:
    postgresql = {
        "user": "user",
        "host": "db",
        "password": "password",
        "port": 5432,
        "db": "books"
    }
except Exception as e:
    logging.exception("Getting credentials for database failed")
