from typing import Union
from pydantic import (
    BaseModel,
    Field,
)
from datetime import datetime


class WeatherData(BaseModel):
    stationId: int
    windDirection: int 
    averageWindSpeedInOneMinute: float
    maxWindSpeedInFiveMinutes: float 
    rainFallInOneHour: float
    rainFallInOneDay: float
    temperature: float 
    humidity: int
    barPressure: float
    createdTime: datetime

    class Config: 
        orm_mode = True


class RecordRequest(BaseModel):
    stationKey: str 
    weatherData: WeatherData

    class Config:
        orm_mode = True
