from app import (
    STATION_BASE_ROUTE, 
)
from fastapi import APIRouter

router = APIRouter(prefix=STATION_BASE_ROUTE)

from .stations import *
