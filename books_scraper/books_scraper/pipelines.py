from sqlalchemy.orm import sessionmaker
from books_scraper.models import Book, Genre, StorySetting, UnsavedBookLink, get_engine, create_all_tables, drop_all_tables
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import NotNullViolation


class SaveBookPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Deletes existing tables
        Creates new tables
        """
        engine = get_engine()
        drop_all_tables(engine)
        create_all_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        # create new session
        session = self.Session()

        book = Book()

        book.has_all_data = False
        book.link = item["link"]
        book.title = item["title"]
        book.author = item["author"]
        book.description = item["description"]
        book.num_pages = item["num_pages"]
        book.num_ratings = item["num_ratings"]
        book.rating_value = item["rating_value"]
        book.date_published = item["date_published"]

        # check that data for genres was extracted
        print(item["genres"])
        if item["genres"] is not None:
            for link, name in item["genres"].items():
                genre = Genre(link=link, name=name)
                # check whether current genre already exists in database
                exist_genre = session.query(
                    Genre).filter_by(link=genre.link).first()
                if exist_genre:
                    genre = exist_genre

                book.genres.append(genre)

        # check that data for story setting was extracted
        if item["settings"] is not None:
            for link, name in item["settings"].items():
                story_setting = StorySetting(link=link, name=name)
                # check whether current genre already exists in database
                exist_story_setting = session.query(
                    StorySetting).filter_by(link=story_setting.link).first()
                if exist_story_setting:
                    genre = exist_story_setting

                book.settings.append(story_setting)

        try:
            # note: don’t need to add genre and story_setting explicitly due to the relationships specified in ORM (book.genres and book.settings
            # the new genre/story_setting (if any) will be created and inserted automatically by SQLAlchemy via the save-update cascade
            print("am going to try to add book to database")
            session.add(book)
            session.commit()
        except IntegrityError as e:
            # will have exception if any of the properties of book are NULL
            print(e)
            # assert isinstance(e.orig, NotNullViolation)
            session.rollback()

            # check to see if this unsaved link is already in database
            exist_unsaved_book_link = session.query(
                UnsavedBookLink).filter_by(link=book.link).first()

            # if the unsaved link isn't in database yet, save it into the database
            if not exist_unsaved_book_link:
                unsaved_book_link = UnsavedBookLink()
                unsaved_book_link.link = book.link
                try:
                    session.add(unsaved_book_link)
                    session.commit()
                except Exception as e:
                    print(e)
                    session.rollback()
        except Exception as e:
            # handle other types of exceptions
            print(e)
            session.rollback()
        finally:
            # close the session
            session.close()

        return item
