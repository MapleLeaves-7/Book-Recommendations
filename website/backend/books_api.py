import sys
from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy.orm import sessionmaker

# add grandparent directory to python path
grandparent_dir = Path(__file__).parents[2]
sys.path.insert(0, str(grandparent_dir))
from db.models import Book, get_engine, Book, Author  # nopep8 (disable autopep8 formatting for this line)

# setup flask app
app = Flask(__name__)
cors = CORS(app)  # allow cors
app.config['CORS_HEADERS'] = 'Content-Type'

# setup sqlalchemy db connection
engine = get_engine()
Session = sessionmaker(bind=engine)


@app.route("/api/book/<int:book_id>")
@cross_origin()
def get_book(book_id):
    book_dict = {}
    with Session.begin() as session:
        book = session.query(Book).filter(Book.id == book_id).first()
        if not book:
            return {"error": "invalid id"}, 400
        if book.title == None or book.description == None or book.has_author == None:
            return {"error": "missing title, description or author"}, 500

        # convert sql book object to python dictionary format
        book_dict = Book.as_dict(book)
        # convert sql author object to python dictionary format to append to book
        book_dict["authors"] = [Author.as_dict(author) for author in book.authors]

    return jsonify(book_dict)


@app.route("/api/book/similar_books/<int:book_id>")
@cross_origin()
def get_similar_books(book_id):
    similar_books = []
    with Session.begin() as session:
        book = session.query(Book).filter(Book.id == book_id).first()
        similar_book_ids = [book.similar_book_id for book in book.similar_books]
        print(similar_book_ids)
        for similar_book_id in similar_book_ids:
            similar_book = session.query(Book).filter(Book.id == similar_book_id).first()
            if similar_book:
                # convert sql book object to python dictionary format
                similar_book_dict = Book.as_dict(similar_book)
                # convert sql author object to python dictionary format to append to book
                similar_book_dict["authors"] = [Author.as_dict(author) for author in book.authors]
                similar_books.append(similar_book_dict)
    return jsonify(similar_books)
