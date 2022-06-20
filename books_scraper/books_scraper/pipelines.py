from sqlalchemy.orm import sessionmaker
from books_scraper.models import Book, Genre, StorySetting, UnsavedBookLink, get_engine, create_all_tables, drop_all_tables
from sqlalchemy.exc import IntegrityError
# from psycopg2.errors import NotNullViolation


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

        has_all_data = True
        all_attributes = ["link", "title", "author", "description", "num_pages", "num_ratings", "rating_value", "date_published"]
        # check if attributes are None, if not, sets the attributes
        for attribute in all_attributes:
            # if attribute is None, it would not be attatched to item
            if attribute not in item or not item[attribute]:
                has_all_data = False
                continue
            setattr(book, attribute, item[attribute])

        # check that data for genres was extracted
        if item["genres"] is not None:
            for link, name in item["genres"].items():
                genre = Genre(link=link, name=name)
                # check whether current genre already exists in database
                exist_genre = session.query(
                    Genre).filter_by(link=genre.link).first()
                if exist_genre:
                    genre = exist_genre

                book.genres.append(genre)
        else:
            has_all_data = False

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
        else:
            has_all_data = False

        book.has_all_data = has_all_data
        
        try:
            # note: don’t need to add genre and story_setting explicitly due to the relationships specified in ORM (book.genres and book.settings
            # the new genre/story_setting (if any) will be created and inserted automatically by SQLAlchemy via the save-update cascade
            print("am going to try to add book to database")
            session.add(book)
            session.commit()
            print("i managed to save the book!!")
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
