import secrets
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from database.base import Base
from database.models.stations_users import StationUser


class Station(Base):
    __tablename__ = "stations"

    stationId = Column(Integer, primary_key=True, index=True)
    stationName = Column(String(length=50), unique=True)
    stationPosition = Column(String(length=100))
    stationKey = Column(String(length=100))
    pushingDataIntervalInSeconds = Column(Integer)

    def __init__(self, stationName: str, 
            stationPosition: str, 
            pushingDataIntervalInSeconds: int = 5):
        self.stationName = stationName
        self.stationPosition = stationPosition
        self.stationKey = self.__generate_the_station_key()
        self.pushingDataIntervalInSeconds = pushingDataIntervalInSeconds

        users = relationship("User", secondary="stations_users")

    def __generate_the_station_key(self, secret_key_length: int = 100) -> str:
        return secrets.token_urlsafe(secret_key_length)

    def __repr__(self):
        return f"<Station stationId={self.stationId} stationName={self.stationName}>"
