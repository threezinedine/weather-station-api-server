from fastapi import (
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session
from typing import (
    List,
)

from app.api.v1.stations import router
from app import (
    ALL_STATIONS_ROUTE,
    CREATE_A_STATION_ROUTE,
    ADD_NEW_STATION_ROUTE,
    RESET_STATION_KEY_ROUTE,
    GET_A_STATION_ROUTE,
)
from database.connection import get_session
from app.constants import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
    HTTP_200_OK,
)
from app.schemas import (
    CreateStationRequest,
    ResponseStation,
    AddStationRequest,
    ResetStationKeyRequest,
)
from app.controllers import StationController
from app.auth import verify_token
from app.api.utils import handleStatus


@router.post(CREATE_A_STATION_ROUTE,
            status_code=HTTP_200_OK,
            response_model=ResponseStation
            )
def create_a_new_station(new_station_info: CreateStationRequest, session: Session = Depends(get_session), username: str = Depends(verify_token)):
    station_controller = StationController(session)
    status, station = station_controller.create_new_station(stationName=new_station_info.stationName,
            stationPosition=new_station_info.stationPosition)

    handleStatus(status)

    status, station = station_controller.add_username(stationName=station.stationName, username=username)

    handleStatus(status)

    return station

@router.put(ADD_NEW_STATION_ROUTE,
        status_code=HTTP_200_OK,
        response_model=ResponseStation)
def add_user_for_station(stationInfo: AddStationRequest, session: Session = Depends(get_session), username: str = Depends(verify_token)):
    station_controller = StationController(session)
    status, station = station_controller.add_username_with_station_key(username=username, stationKey=stationInfo.stationKey)

    handleStatus(status)

    return station

@router.put(RESET_STATION_KEY_ROUTE,
        status_code=HTTP_200_OK,
        response_model=ResponseStation)
def reset_station_key(stationInfo: ResetStationKeyRequest, session: Session = Depends(get_session), username: str = Depends(verify_token)):
    station_controller = StationController(session)
    status, station = station_controller.reset_station_key(stationInfo.stationName)

    handleStatus(status)
    return station

@router.get(ALL_STATIONS_ROUTE,
        status_code=HTTP_200_OK, 
        response_model=List[ResponseStation])
def get_all_stations(session: Session = Depends(get_session), username: str = Depends(verify_token)):
    station_controller = StationController(session)

    status, stations = station_controller.get_station_by_username(username=username)

    handleStatus(status)

    return stations

@router.get(GET_A_STATION_ROUTE,
        status_code=HTTP_200_OK,
        response_model=ResponseStation)
def get_a_station(stationName: str, session: Session = Depends(get_session), username: str = Depends(verify_token)):
    station_controller = StationController(session)

    handleStatus(status)
