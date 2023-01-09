from fastapi import (
    HTTPException,
)
from typing import (
    Dict,
)

from tests import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
)
from app.exceptions import HTTP_200_OK


def handleStatus(status: Dict[str, str]):
    if status[STATUS_CODE_KEY] != HTTP_200_OK:
        raise HTTPException(status_code=status[STATUS_CODE_KEY], detail=status[DETAIL_KEY])
