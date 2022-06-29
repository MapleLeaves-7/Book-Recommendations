import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import time

from models import Book, get_engine, Base, create_all_tables
from sqlalchemy import Column, Float, Integer, and_
from sqlalchemy.orm import sessionmaker


# TDIDF model
# class TFIDF(Base):
#     __tablename__ = 'book_tdidf'
#     id = Column(Integer, primary_key=True)
#     book_id = Column(Integer, nullable=False)
#     tdidf = Column(Integer, nullable=False)


class CosineSim(Base):
    __tablename__ = 'cosine_sim'
    id = Column(Integer, primary_key=True)
    book1_id = Column(Integer, nullable=False)
    book2_id = Column(Integer, nullable=False)
    sim = Column(Float, nullable=False)


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


def get_pd_id(df, db_id):
    return df.loc[df['id'] == db_id].index.item()


def get_db_id(df, pd_id):
    return df.iloc[[pd_id]]['id'].item()


with Session.begin() as session:
    df = pd.read_sql(session.query(Book).filter(Book.has_all_data == True).limit(200).statement, session.bind)
    description = df['description']
    print(df)
    print(description)
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
    print(cosine_sim_matrix)

    for idx1, row in enumerate(cosine_sim_matrix):
        book1_id = get_db_id(df, idx1)
        for idx2, sim in enumerate(row):
            if idx2 == 0:
                continue
            print(idx1, idx2, sim)
            book2_id = get_db_id(df, idx2)
            # print(sim)
            book_cosine_sim = CosineSim(book1_id=book1_id, book2_id=book2_id)
            exist_book_cosine_sim = session.query(CosineSim).filter(and_(CosineSim.book1_id == book1_id, CosineSim.book2_id == book2_id)).first()
            if exist_book_cosine_sim:
                book_cosine_sim = exist_book_cosine_sim
            book_cosine_sim.sim = sim
            # print(book_cosine_sim)cosine_sim_id_seq
            session.add(book_cosine_sim)

    # db_id = 19
    # pd_id = get_pd_id(db_id)

    # # Get the pairwsie similarity scores
    # sim_scores = list(enumerate(cosine_sim[pd_id]))
    # print(sim_scores)

    # # Sort the movies based on the similarity scores
    # sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # print(sim_scores)

    # # Get the scores for 10 most similar movies
    # sim_scores = sim_scores[1:11]

    # # Get the movie indices
    # pd_book_indices = [i[0] for i in sim_scores]

    # # Return the top 10 most similar movies
    # print(df['title'].iloc[pd_book_indices])
