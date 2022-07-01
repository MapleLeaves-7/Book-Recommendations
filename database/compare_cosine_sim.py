import numpy as np
from random import randint
import json

from models import Book, get_engine
from sqlalchemy.orm import sessionmaker


def compare_cosine_sim(matrix_filename, output_filename, max_row_iter=None):
    engine = get_engine()
    Session = sessionmaker(bind=engine)

    with Session.begin() as session:
        cosine_sim_matrix = np.load(matrix_filename)
        books_tfidf = []

        for np_id1, row in enumerate(cosine_sim_matrix):
            if max_row_iter is not None and np_id1 >= max_row_iter:
                break
            book1 = session.query(Book).filter(Book.np_id == np_id1).first()
            tfidf_comparision = {
                "id": book1.id,
                "title": book1.title,
                "most_sim": [],
                "related": [],
                "unrelated_random": []
            }

            related_book_np_ids = [book.np_id for book in book1.related_books]

            for np_id2 in related_book_np_ids:
                if np_id2 is None:
                    continue
                sim = cosine_sim_matrix[np_id1][np_id2]
                sim_python = sim.item()
                book = session.query(Book).filter(Book.np_id == np_id2).first()
                tfidf_comparision["related"].append({"id": book.id,
                                                    "title": book.title,
                                                    "sim": sim_python})


            # sort based on similarity    
            cosine_sim_row = list(enumerate(cosine_sim_matrix[np_id1].tolist()))
            cosine_sim_row.sort(key=lambda x: x[1], reverse=True)
            # get 5 most similar books using cosine_sim_matrix
            for np_id2, sim in cosine_sim_row[1:6]:
                book = session.query(Book).filter(Book.np_id == np_id2).first()
                tfidf_comparision["most_sim"].append({"id": book.id,
                                                    "title": book.title,
                                                    "sim": sim})
            

            random_integers = []

            while len(random_integers) < 5:
                random_num = randint(0, len(cosine_sim_matrix) - 1)
                if random_num in related_book_np_ids or random_num == np_id1:
                    continue
                random_integers.append(random_num)

            for np_id2 in random_integers:
                sim = cosine_sim_matrix[np_id1][np_id2]
                sim_python = sim.item()
                book = session.query(Book).filter(Book.np_id == np_id2).first()
                tfidf_comparision["unrelated_random"].append({"id": book.id,
                                                    "title": book.title,
                                                    "sim": sim_python})

            books_tfidf.append(tfidf_comparision)

        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(books_tfidf, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # compare_cosine_sim('cosine_sim_matrix.npy', 'tfidf_comparision_base.json', 200)
    compare_cosine_sim('cosine_sim_matrix_stemmed.npy', 'tfidf_comparision_base_stemmed.json', 200)