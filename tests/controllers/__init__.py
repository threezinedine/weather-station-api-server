from typing import (
    Dict, 
    Union,
    List,
)

from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
)


def assertStatus(status: Dict[str, Union[int, Union[str, None]]], status_code: int, status_detail: str = None):
    assert status[STATUS_CODE_KEY] == status_code
    assert status[DETAIL_KEY] == status_detail


from .user_controller_test import *
from .station_controller_test import *
