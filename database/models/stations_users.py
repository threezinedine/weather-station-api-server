from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
)

from database.base import Base


class StationUser(Base):
    __tablename__ = "stations_users"

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("users.userId"))
    stationId = Column(Integer, ForeignKey("stations.stationId"))
