from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from passlib.hash import pbkdf2_sha256
from datetime import datetime

from database.base import Base


class User(Base):
    __tablename__ = "users"

    userId = Column(Integer, primary_key=True)
    username = Column(String(length=50), unique=True)
    password = Column(String(length=100))
    lastLoginTime = Column(DateTime, default=datetime.utcnow())

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = self._encode_the_password(password)

    def __repr__(self) -> str:
        return f"<User username={self.username}>"

    def _encode_the_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    def is_match(self, password: str) -> bool:
        return pbkdf2_sha256.verify(self.password, password)
