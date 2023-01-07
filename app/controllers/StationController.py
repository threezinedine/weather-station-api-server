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
)
from app.exceptions import (
    HTTP_200_OK,
    DETAIL_KEY,
    STATUS_CODE_KEY,
)


class StationController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_stations(self) -> Tuple[Dict[str, Union[int, Union[str, None]]], List[Station]]:
        return {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}, []
