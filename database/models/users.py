from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256
from datetime import datetime

from database.base import Base
from database.models.stations_users import StationUser


class User(Base):
    __tablename__ = "users"

    userId = Column(Integer, primary_key=True)
    username = Column(String(length=50), unique=True)
    password = Column(String(length=100))
    lastLoginTime = Column(DateTime, default=datetime.utcnow())

    stations = relationship("Station", secondary="stations_users", back_populates="users")

    def __init__(self, username: str, password: str):
        self.username = username
        self.set_new_password(password)

    def __repr__(self) -> str:
        return f"<User username={self.username}>"

    def set_new_password(self, new_password: str) -> None: 
        self.password = self._encode_the_password(new_password)

    def _encode_the_password(self, password: str) -> str:
        return pbkdf2_sha256.hash(password)

    def is_match(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)
