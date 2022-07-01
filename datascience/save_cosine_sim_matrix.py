import time
import sys
from pathlib import Path

import pandas as pd
import numpy as np
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sqlalchemy.orm import sessionmaker

# add parent directory to python path
parent_dir = Path(__file__).parents[0]
sys.path.insert(0, parent_dir)

# add ../nltk_data to nltk path
nltk.data.path.append(str(parent_dir) + "/nltk_data")
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize 

from db.models import Book, get_engine, create_all_tables


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
    ps = PorterStemmer()
    df = pd.read_sql(session.query(Book).filter(Book.description != None).limit(100).statement, session.bind)

    # update numpy index in database
    for index, row in df.iterrows():
        db_id = row['id']
        book = session.query(Book).filter(Book.id == db_id).first()
        if book:
            book.np_id = index
            session.add(book)

    for idx, row in df.iterrows():
        cleaned_description = []
        for word in word_tokenize(row['description']):
            # if word not in stop_words:
            cleaned_description.append(ps.stem(word))
        cleaned_description = " ".join(cleaned_description)
        df.loc[idx, 'description'] = cleaned_description


    description = df['description']

    # create TfidfVectorizer object
    # modify token pattern so that tokens must contain at least one letter
    vectorizer = TfidfVectorizer(token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b')

    # generate matrix of word vectors
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
    np.save('./data/cosine_sim_matrix_stemmed', cosine_sim_matrix)
