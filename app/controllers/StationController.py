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
    OK_STATUS,
    STATION_DOES_NOT_EXIST_STATUS,
    USER_DOES_NOT_EXIST_STATUS,
    STATION_EXIST_STATUS,
)


class StationController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_stations(self) -> Tuple[Dict[str, Union[int, Union[str, None]]], List[Station]]:
        return OK_STATUS, self.session.query(Station).all() 

    def _get_user_by_username(self, username: str) -> Union[User, None]:
        return self.session.query(User).filter(User.username == username).first()

    def create_new_station(self, stationName: str, stationPosition: str, pushingDataIntervalInSeconds: int = 5) -> Tuple[Dict[str, Union[int, Union[str, None]]], Station]:
        status = OK_STATUS
        _, station_with_station_name = self.get_station_by_station_name(stationName=stationName)
        station = None

        if station_with_station_name is None:
            station = Station(stationName=stationName, stationPosition=stationPosition, pushingDataIntervalInSeconds=pushingDataIntervalInSeconds)
            self.session.add(station)
            self.session.commit()
        else:
            status = STATION_EXIST_STATUS
        return status, station

    def get_station_by_station_name(self, stationName: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], Union[Station, None]]:
        status = OK_STATUS
        station = self.session.query(Station).filter(Station.stationName == stationName).first()

        if station is None:
            status = STATION_DOES_NOT_EXIST_STATUS

        return status, station

    def reset_station_key(self, stationName: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], Union[Station, None]]: 
        status = OK_STATUS
        station = self.session.query(Station).filter(Station.stationName == stationName).first()
        if station is not None:
            station.stationKey = station.generate_the_station_key()
            self.session.commit()
        else:
            status = STATION_DOES_NOT_EXIST_STATUS

        return status, station

    def get_station_by_username(self, username: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], List[Station]]:
        status = OK_STATUS

        user = self.session.query(User).filter(User.username == username).first()
        stations = None

        if user is None:
            status = USER_DOES_NOT_EXIST_STATUS
        else:
            stations = user.stations
        
        return status, stations

    def add_username(self, username: str, stationName: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], Station]:
        status = OK_STATUS

        _, station = self.get_station_by_station_name(stationName)
        user = self._get_user_by_username(username)

        if user is not None:
            if station is not None:
                association = StationUser(stationId=station.stationId, userId=user.userId)
                self.session.add(association)
                self.session.commit()
            else:
                status = STATION_DOES_NOT_EXIST_STATUS
                station = None
        else:
            status = USER_DOES_NOT_EXIST_STATUS
            station = None

        return status, station

    def change_pushing_time_interval_in_seconds(self, stationName: str, new_pushingDataIntervalInSeconds: int) -> Tuple[Dict[str, Union[int, Union[str, None]]], Station]:
        status = OK_STATUS
        _, station = self.get_station_by_station_name(stationName)

        if station is not None:
            station.pushingDataIntervalInSeconds = new_pushingDataIntervalInSeconds
            self.session.commit()
        else:
            status = STATION_DOES_NOT_EXIST_STATUS

        return status, station

    def delete_by_station_name(self, stationName: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], None]:
        status = OK_STATUS

        _, station = self.get_station_by_station_name(stationName)

        if station is not None:
            self.session.delete(station)
            self.session.commit()
        else:
            status = STATION_DOES_NOT_EXIST_STATUS

        return status, None

    def delete_relationship(self, stationName: str, username: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], None]:
        status = OK_STATUS

        _, station = self.get_station_by_station_name(stationName)
        user = self._get_user_by_username(username)

        if user is None:
            status = USER_DOES_NOT_EXIST_STATUS
        else:
            if station is not None:
                user.stations.remove(station)
                self.session.commit()
            else:
                status = STATION_DOES_NOT_EXIST_STATUS

        return status, None
