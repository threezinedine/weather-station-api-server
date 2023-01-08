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

    def get_all_records(self) -> Tuple[Dict[str, Union[int, Union[str, None]]], Record]:
        return OK_STATUS, self.session.query(Record).all()
