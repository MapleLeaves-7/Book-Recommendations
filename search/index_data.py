import sys
from pathlib import Path
import argparse

import meilisearch
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_

# add parent directory to python path
parent_dir = Path(__file__).parents[1]
sys.path.insert(0, str(parent_dir))

from db.models import Book, Author, get_engine, create_all_tables  # nopep8 (disable autopep8 formatting for this line)


engine = get_engine()
create_all_tables(engine)
Session = sessionmaker(bind=engine)
client = meilisearch.Client('http://127.0.0.1:7700')


def get_processed_books(num_books=3000, get_all=False):
    """
    Gets books from database. 
    If get_all is set to True, all the books will get retrieved and num_books will be ignored.
    If get_all is set to False, number of books specified in num_books will be retrieved.
    """
    all_books = []
    with Session.begin() as session:
        # get books which either have all data, or have title, description and author
        if get_all:
            books = session.query(Book).filter(
                or_(Book.has_all_data,
                    and_(Book.title != None, Book.description != None, Book.has_author == True)
                    )).all()
        else:
            books = session.query(Book).filter(
                or_(Book.has_all_data,
                    and_(Book.title != None, Book.description != None, Book.has_author == True)
                    )).limit(num_books)

        for book in books:
            # convert sql book object to python dictionary format
            book_dict = Book.as_dict(book)
            # convert sql author object to python dictionary format to append to book
            book_dict["authors"] = [Author.as_dict(author) for author in book.authors]
            all_books.append(book_dict)

    return all_books


def index_data(index_all=False, num_books=500, batch_num=500):
    """
    Indexes number of books specified into meilisearch in batches.
    index_all: If true, indexes all the books in database into meilisearch and num_books argument will be ignored.
    num_books: Only used when index_all is False. Specifies the number of books to index into database
    batch_num: Specifies the batch size of the books to be indexed.
    """
    all_books = get_processed_books(num_books=num_books, get_all=index_all)
    i = 0
    while i < len(all_books):
        client.index("books").add_documents(all_books[i:i+batch_num])
        i += batch_num

    return all_books


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Index book data into meilisearch.')
    parser.add_argument('-a', '--all', action='store_true', dest='all')
    parser.add_argument('-n', '--num_books', type=int, default=500)
    parser.add_argument('-b', '--batch_num', type=int, default=500)
    args = parser.parse_args()

    index_data(index_all=args.all, num_books=args.num_books, batch_num=args.batch_num)
