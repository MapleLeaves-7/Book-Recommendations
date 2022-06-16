from sqlalchemy_test import BookMetadata, engine, Base

Base.metadata.create_all(engine)