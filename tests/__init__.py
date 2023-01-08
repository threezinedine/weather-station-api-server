from sqlalchemy.orm import (
    sessionmaker,
    Session,
)
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


def clean_database(session: Session):
    session.query(User).delete()
    session.query(Station).delete()
    session.query(StationUser).delete()
    session.query(Record).delete()
    session.commit()
    session.close()



from .api.v1 import *
from .controllers import *
