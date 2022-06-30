# add parent directory to path
from inspect import getsourcefile
import os.path
import sys
current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

from database.models import Book, Author, get_engine, create_all_tables
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
import json

engine = get_engine()
create_all_tables(engine)
Session = sessionmaker(bind=engine)

with Session.begin() as session:
    # get books which either have all data, or have title, description and author
    books = session.query(Book).filter(
        or_(Book.has_all_data, 
            and_(Book.title != None, Book.description != None, Book.has_author == True)
            )).limit(100)
    
    all_books = []
    for book in books:
        # convert sql book object to python dictionary format
        book_dict = Book.as_dict(book)
        # convert sql author object to python dictionary format to append to book
        book_dict["authors"] = [Author.as_dict(author) for author in book.authors]
        all_books.append(book_dict)

    with open('books.json', 'w') as f:
        json.dump(all_books, f, indent=4)