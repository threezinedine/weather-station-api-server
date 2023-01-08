from sqlalchemy import desc
from sqlalchemy.orm import (
    Session,
)
from typing import (
    List, 
    Dict,
    Union,
    Tuple,
)

from database.models import (
    Record,
    Station,
)

from app.exceptions import (
    OK_STATUS,
    WRONG_STATION_KEY_STATUS,
    STATION_DOES_NOT_EXIST_STATUS,
)


class RecordController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_records(self) -> Tuple[Dict[str, Union[int, Union[str, None]]], List[Record]]:
        return OK_STATUS, self.session.query(Record).all()

    def create_new_record(self, stationKey: str, **kwargs) -> Tuple[Dict[str, Union[int, Union[str, None]]], Record]:
        status = OK_STATUS
        record = None
        station = self.session.query(Station).filter(Station.stationId == kwargs["stationId"]).first()

        if station is not None:
            if station.stationKey == stationKey:
                record = Record(**kwargs) 
                self.session.add(record)
                self.session.commit()
            else:
                status = WRONG_STATION_KEY_STATUS
        else:
            status = STATION_DOES_NOT_EXIST_STATUS
        return status, record

    def get_all_records_from_station(self, stationName: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], List[Record]]:
        status = OK_STATUS
        records = None

        station = self.session.query(Station).filter(Station.stationName == stationName).first()
        if station is None:
            status = STATION_DOES_NOT_EXIST_STATUS
        else:
            records = station.records

        return status, records

    def get_latest_record_from_station(self, stationName: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], Record]:
        status = OK_STATUS
        station = self.session.query(Station).filter(Station.stationName == stationName).first()
        latest_record = self.session.query(Record).filter(Record.stationId == station.stationId).order_by(desc(Record.createdTime)).first()

        return status, latest_record
