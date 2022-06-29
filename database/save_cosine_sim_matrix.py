import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import time

from models import Book, get_engine, create_all_tables
from sqlalchemy.orm import sessionmaker


engine = get_engine()
create_all_tables(engine)
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


with Session.begin() as session:
    df = pd.read_sql(session.query(Book).filter(Book.description != None).statement, session.bind)
    for index, row in df.iterrows():
        db_id = row['id']
        book = session.query(Book).filter(Book.id == db_id).first()
        if book:
            book.np_id = index
            session.add(book)

    description = df['description']

    # Create TfidfVectorizer object
    vectorizer = TfidfVectorizer()

    # Generate matrix of word vectors
    tfidf_matrix = vectorizer.fit_transform(description)

    # feature_names = vectorizer.get_feature_names_out()
    # dense = tfidf_matrix.todense()
    # denselist = dense.tolist()
    # df = pd.DataFrame(denselist, columns=feature_names)
    # print(df)

    cosine_sim_matrix = get_linear_kernel(tfidf_matrix)
    # get_cosine_sim(tfidf_matrix)
    # print(cosine_sim_matrix)
    # print(type(cosine_sim_matrix))
    np.save('cosine_sim_matrix', cosine_sim_matrix)
