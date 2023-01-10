from pydantic import BaseModel


class WeatherData(BaseModel):
    windDirection: int 

