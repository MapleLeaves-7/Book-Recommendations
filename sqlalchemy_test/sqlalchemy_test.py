from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, String, Date, Integer, Boolean, Float
from sqlalchemy_utils import database_exists, create_database
import datetime
import os

"""
class book_metadata
    id bigserial
    link
    has_all_data
    title
    author
    book_description
    page_count
    rating_value
    num_ratings
    num_reviews
    date_published
"""

def get_engine(user, host, port, db, password=""):
    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, echo=True)
    return engine
    
engine = get_engine(os.getenv("USERNAME"), os.getenv("HOSTNAME"), os.getenv("PORT"), "books")
Base = declarative_base()
class BookMetadata(Base):
    __tablename__ = 'books_metadata'
    id=Column(Integer(), primary_key=True)
    link=Column(String(), nullable=False, unique=True)
    has_all_data=Column(Boolean(), nullable=False)
    title=Column(String(100))
    author=Column(String(50))
    book_description=Column(String(50))
    num_pages=Column(Integer())
    num_ratings=Column(Integer())
    rating_value=Column(Float(5))
    date_published=Column(Date(), default=datetime.date.today())

    def __repr__(self):
        return f"id={self.id}, link={self.link}, has_all_data={self.has_all_data} title={self.title}"

