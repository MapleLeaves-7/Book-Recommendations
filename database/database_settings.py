import os
import logging

try:
    postgresql = {
        "user": os.getenv("USERNAME"),
        "host": os.getenv("HOSTNAME"),
        "password": os.getenv("PASSWORD"),
        "port": os.getenv("PORT"),
        "db": "books"
        # "db": "books_test"
    }
except Exception as e:
    logging.exception("Getting credentials for database failed")
