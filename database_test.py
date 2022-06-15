from typing import final
import psycopg2
import os
import json

hostname = os.getenv('HOSTNAME')
database = "books"
username = os.getenv('USERNAME')
port_id = os.getenv('PORT')
conn = None
cur = None

try:
    conn = psycopg2.connect(host=hostname,
                            dbname=database,
                            user=username,
                            port=port_id)

    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS books_metadata')
    create_script = '''CREATE TABLE IF NOT EXISTS books_metadata (
                            id BIGSERIAL NOT NULL PRIMARY KEY,
                            link TEXT NOT NULL,
                            has_all_data BOOL NOT NULL,
                            title TEXT,
                            author TEXT,
                            book_description TEXT,
                            page_count INT,
                            rating_value FLOAT,
                            num_ratings INT,
                            num_reviews INT,
                            settings JSON,
                            date_published DATE,
                            genres JSON
                        )'''
    cur.execute(create_script)

    insert_script = 'INSERT INTO books_metadata ( link, has_all_data, title, author, book_description, page_count, rating_value, num_ratings, num_reviews, settings, date_published, genres) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    settings = json.dumps([
        {
            "link": "/places/850-london-england",
            "name": "London, England"
        },
        {
            "link": "/places/853-england",
            "name": "England"
        }
    ])
    genres = json.dumps([
        {
            "link": "/genres/fiction",
            "name": "Fiction"
        },
        {
            "link": "/genres/mystery",
            "name": "Mystery"
        }

    ])
    insert_data = (
        "https://www.goodreads.com/book/show/22557272-the-girl-on-the-train",
        True,
        "The Girl on the Train",
        "Paula Hawkins",
        "Rachel catches the same commuter train every morning. She knows it will wait at the same signal each time, overlooking a row of back gardens. She’s even started to feel like she knows the people who live in one of the houses. “Jess and Jason,” she calls them. Their life—as she sees it—is perfect. If only Rachel could be that happy. And then she sees something shocking. It’s only a minute until the train moves on, but it’s enough. Now everything’s changed. Now Rachel has a chance to become a part of the lives she’s only watched from afar. Now they’ll see; she’s much more than just the girl on the train...",
        325,
        3.95,
        2521434,
        117557,
        settings,
        "2022-06-21",
        genres
    )

    cur.execute(insert_script, insert_data)

    insert_data = (
        "https://www.goodreads.com/book/show/22557272-the-girl-on-the-train",
        False,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None
    )

    cur.execute(insert_script, insert_data)

    conn.commit()

except Exception as e:
    print(e)
finally:
    if conn:
        conn.close()
    if cur:
        cur.close()
