import time
import sys
from pathlib import Path

import pandas as pd
import numpy as np
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sqlalchemy import or_, and_, update
from sqlalchemy.orm import sessionmaker

# add parent directory to python path
parent_dir = Path(__file__).parents[1]
sys.path.insert(0, str(parent_dir))

# add ../nltk_data to nltk path
nltk.data.path.append("./nltk_data")
from nltk.stem import PorterStemmer  # nopep8 (disable autopep8 formatting for this line)
from nltk.tokenize import word_tokenize  # nopep8 (disable autopep8 formatting for this line)

from db.models import Book, get_engine, create_all_tables, BookSimilarBook  # nopep8 (disable autopep8 formatting for this line)


engine = get_engine()
create_all_tables(engine)
Session = sessionmaker(bind=engine)


def get_linear_kernel(tfidf_matrix):
    # Record start time
    start = time.time()

    # Compute cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Print cosine similarity matrix
    # print(cosine_sim)

    # Print time taken
    print("Time taken: %s seconds" % (time.time() - start))
    return cosine_sim


def get_cosine_sim(tfidf_matrix):
    # Record start time
    start = time.time()

    # Compute cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Print cosine similarity matrix
    # print(cosine_sim)

    # Print time taken
    print("Time taken: %s seconds" % (time.time() - start))
    return cosine_sim


def get_cosine_sim_matrix(get_all=False, num_books=100, output_matrix=True, save_into_db=True):
    """
    save_all:
        If true, similarity of all the books will be calculated and num_books will be ignored.
        If False, similarity of number of books specified in num_books will be calculated.
    output_matrix: If true, matrix will be saved as numpy file under data/ folder.
    """
    df = None
    with Session.begin() as session:
        print("resetting all the numpy values...")
        # reset all numpy_id values in book table to be NULL
        session.execute(update(Book).values(np_id=None))

        ps = PorterStemmer()
        print("retrieving books from database...")
        if get_all:
            df = pd.read_sql(session.query(Book).filter(
                or_(Book.has_all_data,
                    and_(Book.title != None, Book.description != None, Book.has_author == True)
                    )).statement, session.bind)
        else:
            df = pd.read_sql(session.query(Book).filter(
                or_(Book.has_all_data,
                    and_(Book.title != None, Book.description != None, Book.has_author == True)
                    )).limit(num_books).statement, session.bind)

        print("updating numpy index in database...")
        # update numpy index in database
        for index, row in df.iterrows():
            db_id = row['id']
            book = session.query(Book).filter(Book.id == db_id).first()
            if book:
                book.np_id = index
                session.add(book)

    print("cleaning description...")
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

    print("getting tfidf matrix...")
    # generate matrix of word vectors
    tfidf_matrix = vectorizer.fit_transform(description)

    # feature_names = vectorizer.get_feature_names_out()
    # dense = tfidf_matrix.todense()
    # denselist = dense.tolist()
    # df = pd.DataFrame(denselist, columns=feature_names)
    # print(df)

    print("calculating cosine similarity...")
    cosine_sim_matrix = get_linear_kernel(tfidf_matrix)

    print("outputting numpy matrix...")
    if output_matrix:
        np.save('./data/cosine_sim_matrix_stemmed', cosine_sim_matrix)

    if save_into_db:
        save_all_similar_books(cosine_sim_matrix=cosine_sim_matrix)


def save_all_similar_books(cosine_sim_matrix):
    """
    Get the cosine similarity matrix and save books similar to each book into database. 
    """
    print("saving similar books into database...")
    print(f"there are {len(cosine_sim_matrix)} books to save")
    for np_id, row in enumerate(cosine_sim_matrix):
        print(f"current np id: {np_id}")
        save_one_similar_books(np_id, row)


def save_one_similar_books(current_np_id, cosine_sim_row):
    """
    Get current book's numpy id and numpy array row of similarity scores.
    Calculate top 10 most similar books to current book and save it into the database.
    """
    with Session.begin() as session:
        # get book with the current numpy id
        current_book = session.query(Book).filter(Book.np_id == current_np_id).first()

        print(f"saving similar books for book id: {current_book.id}")
        # sort based on similarity
        cosine_sim_row = list(enumerate(cosine_sim_row.tolist()))
        cosine_sim_row.sort(key=lambda x: x[1], reverse=True)
        # get 10 most similar books using cosine_sim_matrix
        for np_id2, sim in cosine_sim_row[1:11]:
            # skip those that have similarity 0
            if sim == 0:
                break

            similar_book = session.query(Book).filter(Book.np_id == np_id2).first()
            new_book_similar_book = BookSimilarBook(current_book_id=current_book.id, similar_book_id=similar_book.id)
            # check if a row mapping these 2 books already exists
            exists_book_similar_book = session.query(BookSimilarBook).filter(and_(BookSimilarBook.current_book_id == current_book.id,
                                                                                  BookSimilarBook.similar_book_id == similar_book.id)).first()
            if exists_book_similar_book:
                new_book_similar_book = exists_book_similar_book
            new_book_similar_book.sim = sim
            session.add(new_book_similar_book)


if __name__ == "__main__":
    get_cosine_sim_matrix(num_books=200, output_matrix=False)
