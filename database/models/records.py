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

    def __repr__(self) -> str:
        return f"<Record recordId={self.recordId} createdTime={self.createdTime}>"
