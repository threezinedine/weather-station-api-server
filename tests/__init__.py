from sqlalchemy.orm import (
    sessionmaker,
    Session,
)
from sqlalchemy.engine import create_engine
from typing import (
    Dict, 
    Union,
    List,
)
from sqlalchemy.orm import Session

from database.base import Base

from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
)
from database.models import (
    User,
    Station,
    StationUser,
    Record,
)
from app.controllers import (
    UserController,
    StationController,
    RecordController,
)

FIRST_TEST_USER_USERNAME = "threezinedine"
FIRST_TEST_USER_PASSWORD = "threezinedine1"
SECOND_TEST_USER_USERNAME = "threezinedineadasdf"
SECOND_TEST_USER_PASSWORD = "daffasdgasd"
FIRST_TEST_USER_WRONG_USERNAME = "threezinedine2"
NEW_TEST_USER_PASSWORD = "threezinedineadfab"
FIRST_TEST_USER_NEW_USERNAME = "testing_changed_username"
FIRST_TEST_USER_NEW_PASSWORD = "testing_changed_password"

FIRST_TEST_STATION_STATION_NAME = "Ha Noi"
FIRST_TEST_STATION_STATION_POSITION = "Dong Da, Ha Noi"
FIRST_TEST_STATION_WRONG_STATION_NAME = "HA Noi"
SECOND_TEST_STATION_STATION_NAME = "Bac Ninh"
SECOND_TEST_STATION_STATION_POSITION = "Gia Binh, Bac Ninh"
TEST_STATION_DEFAULT_PUSHING_DATA_INTERVAL_IN_SECONDS = 5
TEST_STATION_PUSHING_DATA_INTERVAL_IN_SECONDS = 10


FIRST_RECORD_DATA = dict(windDirection=1,
                    averageWindSpeedInOneMinute=2.3,
                    maxWindSpeedInFiveMinutes=3.4,
                    rainFallInOneHour=23.1,
                    rainFallInOneDay=13.2,
                    temperature=34.23,
                    humidity=23,
                    barPressure=-123.00,
                    createdTime="2023-01-08 18:54:12"
                    )
SECOND_RECORD_DATA = dict(windDirection=3,
                    averageWindSpeedInOneMinute=4.3,
                    maxWindSpeedInFiveMinutes=13.4,
                    rainFallInOneHour=223.1,
                    rainFallInOneDay=213.2,
                    temperature=24.23,
                    humidity=21,
                    barPressure=123.00,
                    createdTime="2023-01-09 18:54:12"
                    )
FIRST_RECORD_TESTING = dict(stationId=1, **FIRST_RECORD_DATA)
FIRST_WRONG_STATIONID_RECORD_TESTING = dict(stationId=2, **FIRST_RECORD_DATA)
SECOND_RECORD_TESTING = dict(stationId=1, **SECOND_RECORD_DATA)

FIRST_STATION_WRONG_STATION_KEY = "asfagfaodhfahi29183alsdkjfafq0h"


def assertStatus(status: Dict[str, Union[int, Union[str, None]]], reference_status: Dict[str, Union[int, Union[str, None]]]):
    assert status[STATUS_CODE_KEY] == reference_status[STATUS_CODE_KEY]
    assert status[DETAIL_KEY] == reference_status[DETAIL_KEY]

def assertUser(user: User, username: str, password: str):
    assert user.username == username
    assert user.is_match(password)

def assertStation(station: Station, stationName: str, stationPosition: str, pushingDataIntervalInSeconds: int = 5):
    assert station.stationName == stationName
    assert station.stationPosition == stationPosition
    assert station.pushingDataIntervalInSeconds == pushingDataIntervalInSeconds

def assertRecord(record: Record, kwargs):
    for key, value in kwargs.items():
        if key != "createdTime":
            assert getattr(record, key) == value
        else:
            assert str(getattr(record, key)) == value

def createAnUserBy(controller: UserController):
    controller.create_new_user(username=FIRST_TEST_USER_USERNAME, password=FIRST_TEST_USER_PASSWORD)

def createTwoUsersBy(controller: UserController):
    createAnUserBy(controller)
    controller.create_new_user(username=SECOND_TEST_USER_USERNAME, password=SECOND_TEST_USER_PASSWORD)

def createAStationBy(controller: StationController):
    return controller.create_new_station(FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

def createTwoStationsBy(controller: StationController):
    createAStationBy(controller)
    controller.create_new_station(SECOND_TEST_STATION_STATION_NAME, SECOND_TEST_STATION_STATION_POSITION)

def creataAStationAndAnUserBy(user_controller: UserController, station_controller: StationController):
    createAnUserBy(user_controller)
    return createAStationBy(station_controller)

def createAStationAndAnUserAndAddRelationshipBy(user_controller: UserController, station_controller: StationController):
    createAnUserBy(user_controller)
    createAStationBy(station_controller)
    station_controller.add_username(username=FIRST_TEST_USER_USERNAME, stationName=FIRST_TEST_STATION_STATION_NAME)

def createAStationWithExampleRecordBy(station_controller: StationController, record_controller: RecordController):
    _, station = createAStationBy(station_controller)
    return record_controller.create_new_record(stationKey=station.stationKey, **FIRST_RECORD_TESTING)

def createAStationWithTwoExampleRecordsBy(station_controller: StationController, record_controller: RecordController):
    _, station = createAStationBy(station_controller)
    record_controller.create_new_record(stationKey=station.stationKey, **FIRST_RECORD_TESTING)
    record_controller.create_new_record(stationKey=station.stationKey, **SECOND_RECORD_TESTING)



engine = create_engine("sqlite:///testing_database.db")
TestingLocalSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_testing_session():
    try:
        Base.metadata.create_all(engine)
        session = TestingLocalSession()
        yield session
    finally:
        session.close()


def clean_database(session: Session):
    session.query(User).delete()
    session.query(Station).delete()
    session.query(StationUser).delete()
    session.query(Record).delete()
    session.commit()
    session.close()



from .api.v1 import *
from .controllers import *
