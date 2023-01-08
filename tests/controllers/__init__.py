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
from app.controllers import (
    UserController,
    StationController,
)

FIRST_TEST_USER_USERNAME = "threezinedine"
FIRST_TEST_USER_PASSWORD = "threezinedine1"
SECOND_TEST_USER_USERNAME = "threezinedineadasdf"
SECOND_TEST_USER_PASSWORD = "daffasdgasd"
FIRST_TEST_USER_WRONG_USERNAME = "threezinedine2"
NEW_TEST_USER_PASSWORD = "threezinedineadfab"
FIRST_TEST_USER_NEW_USERNAME = "testing_changed_username"
FIRST_TEST_USER_NEW_PASSWORD = "testing_changed_password"

TEST_STATION_NAME = "Ha Noi"
TEST_STATION_POSITION = "Dong Da, Ha Noi"
TEST_STATION_WRONG_STATION_NAME = "HA Noi"
TEST_STATION_DEFAULT_PUSHING_DATA_INTERVAL_IN_SECONDS = 5


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

def createAnUserBy(controller: UserController):
    controller.create_new_user(username=FIRST_TEST_USER_USERNAME, password=FIRST_TEST_USER_PASSWORD)

def createTwoUsersBy(controller: UserController):
    createAnUserBy(controller)
    controller.create_new_user(username=SECOND_TEST_USER_USERNAME, password=SECOND_TEST_USER_PASSWORD)

def createAStationBy(controller: StationController):
    return controller.create_new_station(TEST_STATION_NAME, TEST_STATION_POSITION)

def creataAStationAndAnUserBy(user_controller: UserController, station_controller: StationController):
    createAnUserBy(user_controller)
    return createAStationBy(station_controller)

def createAStationAndAnUserAndAddRelationshipBy(user_controller: UserController, station_controller: StationController):
    createAnUserBy(user_controller)
    createAStationBy(station_controller)
    station_controller.add_username(username=FIRST_TEST_USER_USERNAME, stationName=TEST_STATION_NAME)

from .user_controller_test import *
from .station_controller_test import *
