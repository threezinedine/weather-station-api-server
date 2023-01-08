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
    User,
    StationUser,
)
from app.exceptions import (
    HTTP_200_OK,
    DETAIL_KEY,
    STATUS_CODE_KEY,
    STATION_DOES_NOT_EXIST_STATUS_CODE,
    STATION_DOES_NOT_EXIST_DETAIL,
    STATION_EXIST_DETAIL,
    STATION_EXIST_STATUS_CODE,
    USERNAME_DOES_NOT_EXISTED_STATUS_CODE,
    USERNAME_DOES_NOT_EXISTED_DETAIL,
)


class StationController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_stations(self) -> Tuple[Dict[str, Union[int, Union[str, None]]], List[Station]]:
        return {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}, self.session.query(Station).all() 

    def _get_user_by_username(self, username: str) -> Union[User, None]:
        return self.session.query(User).filter(User.username == username).first()

    def create_new_station(self, stationName: str, stationPosition: str, pushingDataIntervalInSeconds: int = 5) -> Tuple[Dict[str, Union[int, Union[str, None]]], Station]:
        status = {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}
        _, station_with_station_name = self.get_station_by_station_name(stationName=stationName)
        station = None

        if station_with_station_name is None:
            station = Station(stationName=stationName, stationPosition=stationPosition, pushingDataIntervalInSeconds=pushingDataIntervalInSeconds)
            self.session.add(station)
            self.session.commit()
        else:
            status[STATUS_CODE_KEY] = STATION_EXIST_STATUS_CODE
            status[DETAIL_KEY] = STATION_EXIST_DETAIL
        return status, station

    def get_station_by_station_name(self, stationName: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], Union[Station, None]]:
        status = {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}
        station = self.session.query(Station).filter(Station.stationName == stationName).first()

        if station is None:
            status[STATUS_CODE_KEY] = STATION_DOES_NOT_EXIST_STATUS_CODE
            status[DETAIL_KEY] = STATION_DOES_NOT_EXIST_DETAIL

        return status, station

    def reset_station_key(self, stationName: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], Union[Station, None]]: 
        status = {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}
        station = self.session.query(Station).filter(Station.stationName == stationName).first()
        if station is not None:
            station.stationKey = station.generate_the_station_key()
            self.session.commit()
        else:
            status[STATUS_CODE_KEY] = STATION_DOES_NOT_EXIST_STATUS_CODE
            status[DETAIL_KEY] = STATION_DOES_NOT_EXIST_DETAIL

        return status, station

    def get_station_by_username(self, username: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], List[Station]]:
        status = {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}

        user = self.session.query(User).filter(User.username == username).first()
        stations = None

        if user is None:
            status[STATUS_CODE_KEY] = USERNAME_DOES_NOT_EXISTED_STATUS_CODE
            status[DETAIL_KEY] = USERNAME_DOES_NOT_EXISTED_DETAIL
        else:
            stations = user.stations
        
        return status, stations

    def add_username(self, username: str, stationName: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], Station]:
        status = {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}

        _, station = self.get_station_by_station_name(stationName)
        user = self._get_user_by_username(username)

        if user is not None:
            association = StationUser(stationId=station.stationId, userId=user.userId)
            self.session.add(association)
            self.session.commit()
        else:
            status[STATUS_CODE_KEY] = USERNAME_DOES_NOT_EXISTED_STATUS_CODE
            status[DETAIL_KEY] = USERNAME_DOES_NOT_EXISTED_DETAIL
            station = None

        return status, station
