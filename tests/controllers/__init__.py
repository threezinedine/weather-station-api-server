from typing import (
    Dict, 
    Union,
    List,
)

from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
)
from database.models import (
    User,
    Station,
)


def assertStatus(status: Dict[str, Union[int, Union[str, None]]], status_code: int, status_detail: str = None):
    assert status[STATUS_CODE_KEY] == status_code
    assert status[DETAIL_KEY] == status_detail

def assertUser(user: User, username: str, password: str):
    assert user.username == username
    assert user.is_match(password)

def assertStation(station: Station, stationName: str, stationPosition: str, pushingDataIntervalInSeconds: int = 5):
    assert station.stationName == stationName
    assert station.stationPosition == stationPosition
    assert station.pushingDataIntervalInSeconds == pushingDataIntervalInSeconds


from .user_controller_test import *
from .station_controller_test import *
