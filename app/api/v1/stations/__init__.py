from fastapi import APIRouter
from app import STATION_BASE_ROUTE


router = APIRouter(prefix=STATION_BASE_ROUTE, tags=["Stations"])


from .stations import *
