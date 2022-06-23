# add parent directory to path
from models import Book, get_engine
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from inspect import getsourcefile
import os.path
import sys
current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

engine = get_engine()
Session = sessionmaker(bind=engine)


def check_has_all_data():
    with Session.begin() as session:
        books = session.query(Book).filter(and_(Book.has_all_data == False, Book.has_author == True, Book.has_genre == True, Book.has_setting == True,
                                                Book.has_related_books == True, Book.title != None, Book.description != None, Book.num_pages != None,
                                                Book.num_ratings != None, Book.rating_value != None, Book.date_published != None))
        count = 0
        for book in books:
            count += 1
            print(book.title)
        print(count)


def update_has_all_data():
    with Session.begin() as session:
        books = session.query(Book).filter(and_(Book.has_all_data == False, Book.has_author == True, Book.has_genre == True, Book.has_setting == True,
                                                Book.has_related_books == True, Book.title != None, Book.description != None, Book.num_pages != None,
                                                Book.num_ratings != None, Book.rating_value != None, Book.date_published != None))
        for book in books:
            book.has_all_data = True


update_has_all_data()
check_has_all_data()
