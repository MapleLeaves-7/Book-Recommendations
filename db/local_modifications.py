from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from models import Book, Author, StorySetting, Genre, get_engine, create_all_tables, drop_all_tables  # nopep8 (disable autopep8 formatting for this line)

engine = get_engine()
Session = sessionmaker(bind=engine)

# book_links = []
# with Session.begin() as session:
#     books = session.query(Book).filter(Book.title == None).all()
#     count = 0
#     for book in books:
#         print(f"{book.id}: {book.title}")
#         book_links.append(book.link)
#         count += 1
#     print(count)
#     print(len(books))

# print(book_links)
# print(len(book_links))


with Session.begin() as session:
    settings = session.query(StorySetting).all()
    for setting in settings:
        setting.name = setting.name.title()
        print(setting.name)


# with Session.begin() as session:
#     genres = session.query(Genre).all()
#     for genre in genres:
#         genre.name = genre.name.title()
#         print(genre.name)
