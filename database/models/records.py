from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Float,
    ForeignKey,
)

from database.base import Base


class Record(Base):
    __tablename__ = "records"

    recordId = Column(Integer, primary_key=True)
    stationId = Column(Integer, ForeignKey("stations.stationId"))
    windDirection = Column(Integer)
    averageWindSpeedInOneMinute = Column(Float)
    maxWindSpeedInFiveMinutes = Column(Float)
    rainFallInOneHour = Column(Float)
    rainFallInOneDay = Column(Float)
    temperature = Column(Float)
    humidity = Column(Integer)
    barPressure = Column(Float)
    createdTime = Column(DateTime)

    def __init__(self, **kwargs):
        kwargs["createdTime"] = datetime.strptime(kwargs["createdTime"], "%Y-%m-%d %H:%M:%S")
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"<Record recordId={self.recordId} createdTime={self.createdTime}>"
