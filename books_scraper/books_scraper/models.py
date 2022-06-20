from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, Float, Boolean
)
from sqlalchemy_utils import database_exists, create_database
from books_scraper.database_settings import postgresql as db_settings

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


# Association table for many to many relationship between books and genres
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
book_genre = Table('book_genre',
                   Base.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('book_id', Integer, ForeignKey('books.id')),
                   Column('genre_id', Integer, ForeignKey('genres.id')))

# Association table for many to many relationship between books and story settings
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
book_story_setting = Table('book_story_setting',
                           Base.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('book_id', Integer, ForeignKey('books.id')),
                           Column('story_settings', Integer, ForeignKey('story_settings.id')))


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False, unique=True)
    has_all_data = Column(Boolean, nullable=False)
    title = Column(String(150))
    author = Column(String(50))
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


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False, unique=True)
    name = Column(String(50))
    # # M-to-M relationship between books and genres
    # books = relationship('Book', secondary='book_genre', backref='Genre')


class StorySetting(Base):
    __tablename__ = "story_settings"

    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False, unique=True)
    name = Column(String(50))
    # # M-to-M relationship between books and story settings
    # books = relationship(
    #     'Book', secondary='book_story_setting', backref='StorySetting')