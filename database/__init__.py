from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


database_uri = os.environ.get("DATABASE_URI", "sqlite:///database.db")

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    try: 
        db = SessionLocal()
        yield db 
    finally:
        db.close()
