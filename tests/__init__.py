from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine

from database.base import Base


engine = create_engine("sqlite:///testing_database.db")
TestingLocalSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_testing_session():
    try:
        Base.metadata.create_all(engine)
        session = TestingLocalSession()
        yield session
    finally:
        session.close()


from .api.v1 import *
from .controllers import *
