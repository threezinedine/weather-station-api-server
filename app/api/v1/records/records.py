from typing import (
    List,
)
from fastapi import (
    Depends,
)
from sqlalchemy.orm import Session

from app.api.v1.records import router
from app.api.utils import handleStatus
from app.auth import verify_token
from app.controllers import RecordController
from app import (
    CREATE_RECORD_ROUTE,
    GET_THE_LATEST_RECORD_ROUTE,
    GET_ALL_RECORDS_ROUTE,
)
from app.constants import (
    HTTP_200_OK,
)
from database.connection import get_session
from app.schemas import (
    WeatherData,
    RecordRequest,
)


@router.post(CREATE_RECORD_ROUTE,
        status_code=HTTP_200_OK,
        response_model=WeatherData)
def create_a_station(data: RecordRequest, session: Session = Depends(get_session)):
    record_controller = RecordController(session)

    status, record = record_controller.create_new_record(stationKey=data.stationKey, **data.weatherData.dict())
    handleStatus(status)

    return record

@router.get(GET_THE_LATEST_RECORD_ROUTE,
        status_code=HTTP_200_OK,
        response_model=WeatherData
        )
def get_the_latest_record(stationName: str, session: Session = Depends(get_session), username: str = Depends(verify_token)):
    record_controller = RecordController(session)

    status, record = record_controller.get_the_latest_record_by_username_and_station_name(username=username, stationName=stationName)

    handleStatus(status)

    return record

@router.get(GET_ALL_RECORDS_ROUTE,
        status_code=HTTP_200_OK,
        response_model=List[WeatherData])
def get_all_record(stationName: str, session: Session = Depends(get_session), username: str = Depends(verify_token)):
    record_controller = RecordController(session)

    status, records = record_controller.get_all_records_by_username_and_station_name(username=username, stationName=stationName)
    handleStatus(status)

    return records
