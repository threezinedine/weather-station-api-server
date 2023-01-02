from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from database.base import Base


database_uri = os.environ.get("DATABASE_URI", "sqlite:///database.db")

engine = create_engine(database_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try: 
        Base.metadata.create_all(engine)
        db = SessionLocal()
        yield db 
    finally:
        db.close()
