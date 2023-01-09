USER_BASE_ROUTE = "/users"

LOGIN_ROUTE = "/login"
REGISTER_ROUTE = "/register"

LOGIN_FULL_ROUTE = f"{USER_BASE_ROUTE}{LOGIN_ROUTE}"
REGISTER_FULL_ROUTE = f"{USER_BASE_ROUTE}{REGISTER_ROUTE}"

STATION_BASE_ROUTE = "/stations"

ALL_STATIONS_ROUTE = "/"
CREATE_A_STATION_ROUTE = "/"
ADD_NEW_STATION_ROUTE = "/"

ALL_STATIONS_FULL_ROUTE = f"{STATION_BASE_ROUTE}{ALL_STATIONS_ROUTE}"
CREATE_A_STATION_FULL_ROUTE = f"{STATION_BASE_ROUTE}{CREATE_A_STATION_ROUTE}"
ADD_NEW_STATION_FULL_ROUTE = f"{STATION_BASE_ROUTE}{ADD_NEW_STATION_ROUTE}"


from fastapi import APIRouter

router = APIRouter()
