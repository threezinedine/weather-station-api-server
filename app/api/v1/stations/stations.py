from fastapi import (
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.api.v1.stations import router
from app import (
    ALL_STATIONS_ROUTE,
    CREATE_A_STATION_ROUTE,
    ADD_NEW_STATION_ROUTE,
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
)
from app.controllers import StationController
from app.auth import verify_token
from app.api.utils import handleStatus


@router.post(CREATE_A_STATION_ROUTE,
            status_code=HTTP_200_OK,
            response_model=ResponseStation
            )
def get_all_stations(new_station_info: CreateStationRequest, session: Session = Depends(get_session), username: str = Depends(verify_token)):
    station_controller = StationController(session)
    status, station = station_controller.create_new_station(stationName=new_station_info.stationName,
            stationPosition=new_station_info.stationPosition)

    handleStatus(status)

    status, station = station_controller.add_username(stationName=station.stationName, username=username)

    handleStatus(status)

    return station

@router.put(ADD_NEW_STATION_ROUTE,
        status_code=HTTP_200_OK)
def get_all_stations(stationInfo: AddStationRequest, session: Session = Depends(get_session), username: str = Depends(verify_token)):
    station_controller = StationController(session)

    return ""
