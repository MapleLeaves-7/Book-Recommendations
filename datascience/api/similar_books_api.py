import sys
from pathlib import Path

from flask import Flask, jsonify
from sqlalchemy.orm import sessionmaker

# add grandparent directory to python path
grandparent_dir = Path(__file__).parents[2]
sys.path.insert(0, str(grandparent_dir))
from db.models import Book, get_engine, Book  # nopep8 (disable autopep8 formatting for this line)

app = Flask(__name__)
engine = get_engine()
Session = sessionmaker(bind=engine)


@app.route("/api/similar_books/<int:book_id>")
def get_similar_books(book_id):
    similar_books = []
    with Session.begin() as session:
        book = session.query(Book).filter(Book.id == book_id).first()
        similar_book_ids = [book.similar_book_id for book in book.similar_books]
        for similar_book_id in similar_book_ids:
            similar_book = session.query(Book).filter(Book.id == similar_book_id).first()
            if similar_book:
                similar_books.append(Book.as_dict(similar_book))  # convert to dictionary before returning
    return jsonify(similar_books)
