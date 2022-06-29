import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import time
from random import randint
import json

from models import Book, get_engine
from sqlalchemy.orm import sessionmaker


engine = get_engine()
Session = sessionmaker(bind=engine)


def get_linear_kernel(tfidf_matrix):
    # Record start time
    start = time.time()

    # Compute cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Print cosine similarity matrix
    print(cosine_sim)

    # Print time taken
    print("Time taken: %s seconds" % (time.time() - start))
    return cosine_sim


def get_cosine_sim(tfidf_matrix):
    # Record start time
    start = time.time()

    # Compute cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Print cosine similarity matrix
    print(cosine_sim)

    # Print time taken
    print("Time taken: %s seconds" % (time.time() - start))
    return cosine_sim


def get_pd_id(df, db_id):
    row = df.loc[df['id'] == db_id]
    if row.empty:
        return None
    return row.index.item()


def get_db_id(df, pd_id):
    return df.iloc[[pd_id]]['id'].item()


with Session.begin() as session:
    df = pd.read_sql(session.query(Book).filter(Book.description != None).limit(200).statement, session.bind)
    description = df['description']
    all_book_ids = df['id'].to_numpy()
    # Create TfidfVectorizer object
    vectorizer = TfidfVectorizer()

    # Generate matrix of word vectors
    tfidf_matrix = vectorizer.fit_transform(description)

    cosine_sim_matrix = get_linear_kernel(tfidf_matrix)
    # get_cosine_sim(tfidf_matrix)
    books_tfidf = []

    for idx1, row in enumerate(cosine_sim_matrix):
        tfidf_comparision = {
            "id": get_db_id(df, idx1),
            "related": [],
            "unrelated": []
        }
        book1_id = tfidf_comparision["id"]
        book1 = session.query(Book).filter(Book.id == book1_id).first()
        tfidf_comparision["title"] = book1.title
        related_book_pd_ids = [get_pd_id(df, book.id) for book in book1.related_books]

        for idx2 in related_book_pd_ids:
            if idx2 is None:
                continue
            sim = cosine_sim_matrix[idx1][idx2]
            sim_python = sim.item()
            db_id = get_db_id(df, idx2)
            book = session.query(Book).filter(Book.id == db_id).first()
            tfidf_comparision["related"].append({"id": db_id,
                                                 "title": book.title,
                                                 "sim": sim_python})

        random_integers = []

        while len(random_integers) < 5:
            random_num = randint(0, len(cosine_sim_matrix) - 1)
            if random_num in related_book_pd_ids or random_num == idx1:
                continue
            random_integers.append(random_num)

        for idx2 in random_integers:
            sim = cosine_sim_matrix[idx1][idx2]
            sim_python = sim.item()
            db_id = get_db_id(df, idx2)
            book = session.query(Book).filter(Book.id == db_id).first()
            tfidf_comparision["unrelated"].append({"id": db_id,
                                                   "title": book.title,
                                                   "sim": sim_python})

        books_tfidf.append(tfidf_comparision)

    with open('tfidf_comparision.json', 'w', encoding='utf-8') as f:
        json.dump(books_tfidf, f, ensure_ascii=False, indent=4)
