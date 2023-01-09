from fastapi import (
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.api.v1.stations import router
from app import (
    ALL_STATIONS_ROUTE,
    CREATE_A_STATION_ROUTE,
)
from database.connection import get_session
from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
    HTTP_200_OK,
)
from app.schemas import (
    CreateStationRequest,
    ResponseStation,
)
from app.controllers import StationController
from app.auth import verify_token


@router.post(CREATE_A_STATION_ROUTE,
            status_code=HTTP_200_OK,
            response_model=ResponseStation
            )
def get_all_stations(new_station_info: CreateStationRequest, session: Session = Depends(get_session), username: str = Depends(verify_token)):
    station_controller = StationController(session)
    status, station = station_controller.create_new_station(stationName=new_station_info.stationName,
            stationPosition=new_station_info.stationPosition)

    if status[STATUS_CODE_KEY] != HTTP_200_OK:
        raise HTTPException(status_code=status[STATUS_CODE_KEY],
                detail=status[DETAIL_KEY])

    status, station = station_controller.add_username(stationName=station.stationName, username=username)

    if status[STATUS_CODE_KEY] != HTTP_200_OK:
        raise HTTPException(status_code=status[STATUS_CODE_KEY],
                detail=status[DETAIL_KEY])

    return station
