from sqlalchemy import UniqueConstraint, create_engine, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import (
    Integer, String, Date, Float, Boolean
)
from sqlalchemy_utils import database_exists, create_database

# add parent directory to path so that database settings can always be imported properly
from inspect import getsourcefile
import os.path
import sys
current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

from db.db_config import postgresql as db_settings  # nopep8 (disable autopep8 formatting for this line) -> so that import statement does not get moved to the top


Base = declarative_base()


def get_engine():
    user = db_settings["user"]
    password = db_settings["password"]
    host = db_settings["host"]
    port = db_settings["port"]
    db = db_settings["db"]

    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    return create_engine(url)


def create_all_tables(engine):
    Base.metadata.create_all(engine)


def drop_all_tables(engine):
    Base.metadata.drop_all(engine)


# Association table for many to many relationship between books and authors
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
book_author = Table('book_author',
                    Base.metadata,
                    Column('id', Integer, primary_key=True),
                    Column('book_id', Integer, ForeignKey('books.id')),
                    Column('author_id', Integer, ForeignKey('authors.id')))

# Association table for many to many relationship between books and genres
book_genre = Table('book_genre',
                   Base.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('book_id', Integer, ForeignKey('books.id')),
                   Column('genre_id', Integer, ForeignKey('genres.id')))

# Association table for many to many relationship between books and story settings
book_story_setting = Table('book_story_setting',
                           Base.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('book_id', Integer, ForeignKey('books.id')),
                           Column('story_settings', Integer, ForeignKey('story_settings.id')))

# Association table for many to many relationship between books and related books -> related books are crawled from goodreads
book_related_book = Table('book_related_book',
                          Base.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('book_id', Integer, ForeignKey('books.id')),
                          Column('related_book_id', Integer, ForeignKey('books.id')),
                          UniqueConstraint('book_id', 'related_book_id', name='unique_related_books')
                          )

class BookSimilarBook(Base):
    # similar books are based on own recommendations
    __tablename__ = "book_similar_book"

    id = Column(Integer, primary_key=True)
    current_book_id = Column(Integer, ForeignKey('books.id'))
    similar_book_id =  Column(Integer, ForeignKey('books.id'))
    sim = Column(Float) # cosine similarity bewteen books


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False, unique=True)
    # note: has_all_data is false if any of the fields are null, including author, genre, setting and related books
    has_all_data = Column(Boolean, nullable=False)
    has_author = Column(Boolean)
    has_genre = Column(Boolean)
    has_setting = Column(Boolean)
    has_related_books = Column(Boolean)
    title = Column(String(150))
    # M-to-M relationship between books and authors
    authors = relationship('Author', secondary='book_author', backref='Book')
    description = Column(String)
    num_pages = Column(Integer)
    num_ratings = Column(Integer)
    rating_value = Column(Float(5))
    date_published = Column(Date)
    # M-to-M relationship between books and genres
    genres = relationship('Genre', secondary='book_genre', backref='Book')
    # M-to-M relationship between books and story settings
    settings = relationship(
        'StorySetting', secondary='book_story_setting', backref='Book')
    # M-to-M relationship between books and related books (this is a self-referential relationship) -> related books are crawled from goodreads
    related_books = relationship('Book', secondary=book_related_book,
                                 primaryjoin=id == book_related_book.c.book_id,
                                 secondaryjoin=id == book_related_book.c.related_book_id)
    # panda id when the data was first read and processed -> maps to respective row / column in numpy cosine similarity matrix that was dumped out
    np_id = Column(Integer)

    # note: similar books are based on own recommendations
    # contains a list of BookSimilarBook objects where the id of the current book is the same as the current_book_id of BookSimilarBook
    similar_books = relationship('BookSimilarBook', primaryjoin=id==BookSimilarBook.current_book_id)

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns} 


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False, unique=True)
    name = Column(String(50))

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns} 


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False, unique=True)
    name = Column(String(50))

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns} 


class StorySetting(Base):
    __tablename__ = "story_settings"

    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False, unique=True)
    name = Column(String(50))

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns} 


## alternative relation
## add the following 2 lines to the Book class
# current_books = association_proxy("current_book_relations", "current_book")
# similar_books = association_proxy("similar_books_relations", "similar_book")

# class BookSimilarBook(Base):
#     # similar books are based on own recommendations
#     __tablename__ = "book_similar_book"

#     id = Column(Integer, primary_key=True)
#     current_book_id = Column(Integer, ForeignKey('books.id'))
#     similar_book_id =  Column(Integer, ForeignKey('books.id'))
#     sim = Column(Float) # cosine similarity bewteen books

#     current_book = relationship(Book, primaryjoin=(current_book_id == Book.id), backref='similar_books_relations')
#     similar_book = relationship(Book, primaryjoin=(similar_book_id == Book.id), backref='current_book_relations')