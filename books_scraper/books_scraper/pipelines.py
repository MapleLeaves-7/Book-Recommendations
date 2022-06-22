from sqlalchemy.orm import sessionmaker
from books_scraper.models import Book, Genre, StorySetting, get_engine, create_all_tables, drop_all_tables


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
        # don't save book into database if it does not have link
        if "link" not in item:
            return item

        # create new session
        session = self.Session()

        book = Book(link=item["link"], has_all_data=True)

        # check if book was previously saved in database
        exist_book = session.query(Book).filter_by(link=book.link).first()
        if exist_book:
            if exist_book.has_all_data:
                # don't need to save new info if the book exists and already has all data
                return item

            book = exist_book

        attributes = ["title", "author", "description", "num_pages", "num_ratings", "rating_value", "date_published"]

        # check if attributes are None, if not, sets the attributes
        for attribute in attributes:
            # if attribute is None, it would not be attached to item
            if attribute not in item or not item[attribute]:
                book.has_all_data = False
                continue
            setattr(book, attribute, item[attribute])

        for attribute in ["has_genre", "has_setting", "has_related_books"]:
            setattr(book, attribute, True)

        if "genres" in item:  # check that data for genres was extracted
            for link, name in item["genres"].items():
                genre = Genre(link=link, name=name)
                # check whether current genre already exists in database
                exist_genre = session.query(Genre).filter_by(link=genre.link).first()
                if exist_genre:
                    genre = exist_genre

                book.genres.append(genre)
        else:
            book.has_all_data = False
            book.has_genre = False

        if "settings" in item:  # check that data for story setting was extracted
            for link, name in item["settings"].items():
                story_setting = StorySetting(link=link, name=name)
                # check whether current genre already exists in database
                exist_story_setting = session.query(StorySetting).filter_by(link=story_setting.link).first()
                if exist_story_setting:
                    story_setting = exist_story_setting

                book.settings.append(story_setting)
        else:
            book.has_all_data = False
            book.has_setting = False

        if "related_book_links" in item:
            for link in item["related_book_links"]:
                related_book = session.query(Book).filter_by(link=link).first()

                # save related book into database table if it doesn't exist yet
                if not related_book:
                    new_related_book = Book(link=link, has_all_data=False)

                    try:
                        # save related book into table
                        session.add(new_related_book)
                        session.commit()
                    except Exception as e:
                        print(e)
                        session.rollback()
                        # continue to the next link if current link fails
                        continue
                    else:
                        # get related book that was just saved into database
                        related_book = session.query(Book).filter_by(link=link).first()

                # check that related book exists before appending it to current book
                if related_book:
                    book.related_books.append(related_book)
        else:
            book.has_all_data = False
            book.has_related_books = False

        try:
            # note: don’t need to add genre and story_setting explicitly due to the relationships specified in ORM (book.genres and book.settings
            # the new genre/story_setting (if any) will be created and inserted automatically by SQLAlchemy via the save-update cascade
            print("am going to try to add book to database")
            session.add(book)
            session.commit()
            print("i managed to save the book!!")
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            # close the session
            session.close()

        return item
