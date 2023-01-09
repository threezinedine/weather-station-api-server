from pydantic import BaseModel


class CreateStationRequest(BaseModel):
    stationName: str
    stationPosition: str
    pushingDataIntervalInSeconds: int = 5

    class Config:
        orm_mode = True

class ResponseStation(CreateStationRequest):
    stationId: int
    stationKey: str

class AddStationRequest(BaseModel):
    stationKey: str

    class Config:
        orm_mode = True
