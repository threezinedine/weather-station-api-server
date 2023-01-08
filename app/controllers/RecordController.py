from sqlalchemy.orm import Session
from typing import (
    List, 
    Dict,
    Union,
    Tuple,
)

from database.models import (
    Record,
)

from app.exceptions import (
    OK_STATUS,
)


class RecordController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_records(self) -> Tuple[Dict[str, Union[int, Union[str, None]]], List[Record]]:
        return OK_STATUS, self.session.query(Record).all()

    def create_new_record(self, **kwargs) -> Tuple[Dict[str, Union[int, Union[str, None]]], Record]:
        record = Record(**kwargs) 
        self.session.add(record)
        self.session.commit()

        return OK_STATUS, record
