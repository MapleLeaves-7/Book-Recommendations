import sys
from pathlib import Path

import meilisearch
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_

# add parent directory to python path
parent_dir = Path(__file__).parents[0]
sys.path.insert(0, parent_dir)

from db.models import Book, Author, get_engine, create_all_tables


engine = get_engine()
create_all_tables(engine)
Session = sessionmaker(bind=engine)
client = meilisearch.Client('http://127.0.0.1:7700')

def get_processed_books():
    all_books = []
    with Session.begin() as session:
        # get books which either have all data, or have title, description and author
        books = session.query(Book).filter(
            or_(Book.has_all_data, 
                and_(Book.title != None, Book.description != None, Book.has_author == True)
                )).limit(100)
        
        for book in books:
            # convert sql book object to python dictionary format
            book_dict = Book.as_dict(book)
            # convert sql author object to python dictionary format to append to book
            book_dict["authors"] = [Author.as_dict(author) for author in book.authors]
            all_books.append(book_dict)

    return all_books    

def index_data():
    all_books = get_processed_books()
    client.index("books").add_documents(all_books)
    return all_books

if __name__ == "__main__":
    index_data()