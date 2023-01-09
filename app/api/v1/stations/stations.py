from app.api.v1.stations import router
from app import (
    ALL_STATIONS_ROUTE,
)


@router.get(ALL_STATIONS_ROUTE)
def get_all_stations():
    return ""
