from typing import (
    Dict,
    Union,
    List,
    Tuple,
)
from sqlalchemy.orm import (
    Session,
)

from database.models import (
    Station,
)
from app.exceptions import (
    HTTP_200_OK,
    DETAIL_KEY,
    STATUS_CODE_KEY,
    STATION_DOES_NOT_EXIST_STATUS_CODE,
    STATION_DOES_NOT_EXIST_DETAIL,
)


class StationController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_stations(self) -> Tuple[Dict[str, Union[int, Union[str, None]]], List[Station]]:
        return {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}, self.session.query(Station).all() 

    def create_new_station(self, stationName: str, stationPosition: str, pushingDataIntervalInSeconds: int = 5) -> Tuple[Dict[str, Union[int, Union[str, None]]], Station]:
        station = Station(stationName=stationName, stationPosition=stationPosition, pushingDataIntervalInSeconds=pushingDataIntervalInSeconds)
        self.session.add(station)
        self.session.commit()
        return {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}, station

    def get_station_by_station_name(self, stationName: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], Union[Station, None]]:
        status = {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}
        station = self.session.query(Station).filter(Station.stationName == stationName).first()

        if station is None:
            status[STATUS_CODE_KEY] = STATION_DOES_NOT_EXIST_STATUS_CODE
            status[DETAIL_KEY] = STATION_DOES_NOT_EXIST_DETAIL

        return status, station
