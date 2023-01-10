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
        status_code=HTTP_200_OK)
def create_a_station(data: RecordRequest, session: Session = Depends(get_session)):
    record_controller = RecordController(session)

    status, record = record_controller.create_new_record(stationKey=data.stationKey, **data.weatherData.dict())
    handleStatus(status)

    return record
