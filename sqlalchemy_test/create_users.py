from sqlalchemy_test import BookMetadata, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()

local_session = Session(bind=engine)

new_book = BookMetadata(link="test", has_all_data=True)
local_session.add(new_book)
local_session.commit()