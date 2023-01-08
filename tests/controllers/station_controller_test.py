import unittest
from typing import (
    Dict,
    Union,
)

from database.models import (
    User,
    Station,
    StationUser,
)
from app.controllers import (
    StationController,
    UserController,
)
from tests import (
    get_testing_session,
)
from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
    HTTP_200_OK,
    STATION_DOES_NOT_EXIST_DETAIL,
    STATION_DOES_NOT_EXIST_STATUS_CODE,
    STATION_EXIST_STATUS_CODE,
    STATION_EXIST_DETAIL,
    USERNAME_DOES_NOT_EXISTED_STATUS_CODE,
    USERNAME_DOES_NOT_EXISTED_DETAIL,
)
from tests.controllers import (
    assertStatus,
    assertStation,
    TEST_STATION_NAME,
    TEST_STATION_POSITION,
    TEST_STATION_WRONG_STATION_NAME,
    TEST_STATION_DEFAULT_PUSHING_DATA_INTERVAL_IN_SECONDS,
    FIRST_TEST_USER_USERNAME,
    FIRST_TEST_USER_PASSWORD,
    createAStationBy,
    creataAStationAndAnUserBy,
    createAStationAndAnUserAndAddRelationshipBy,
)


class StationControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.station_controller = StationController(self.session)
        self.user_controller = UserController(self.session)

    def tearDown(self):
        self.session.query(User).delete()
        self.session.query(Station).delete()
        self.session.query(StationUser).delete()
        self.session.commit()
        self.session.close()

    def assertStation(self, station: Station, stationName: str, 
            stationPosition: str, pushingDataIntervalInSeconds: int = TEST_STATION_DEFAULT_PUSHING_DATA_INTERVAL_IN_SECONDS):
        assert station.stationName == stationName
        assert station.stationPosition == stationPosition
        assert station.pushingDataIntervalInSeconds == pushingDataIntervalInSeconds

    def test_given_no_station_is_created_when_querying_all_stations_then_returns_ok_and_empty_array(self):
        status, stations = self.station_controller.get_all_stations()

        assertStatus(status, HTTP_200_OK)
        self.assertListEqual(stations, [])

    def test_given_no_station_is_created_when_creating_new_station_then_returns_ok_and_that_station(self):
        status, station = self.station_controller.create_new_station(stationName=TEST_STATION_NAME, stationPosition=TEST_STATION_POSITION)

        assertStatus(status, HTTP_200_OK)
        assertStation(station, TEST_STATION_NAME, TEST_STATION_POSITION)

    def test_given_a_station_is_created_when_querying_all_stations_then_returns_ok_and_station_list(self):
        createAStationBy(self.station_controller)

        status, stations = self.station_controller.get_all_stations()

        assertStatus(status, HTTP_200_OK)
        assert len(stations) == 1
        assertStation(stations[0], TEST_STATION_NAME, TEST_STATION_POSITION)

    def test_given_a_station_is_created_when_querying_station_by_valid_station_name_then_returns_ok_and_station(self):
        createAStationBy(self.station_controller)

        status, station = self.station_controller.get_station_by_station_name(stationName=TEST_STATION_NAME)

        assertStatus(status, HTTP_200_OK)
        assertStation(station, TEST_STATION_NAME, TEST_STATION_POSITION)

    def test_given_a_station_is_created_when_querying_station_by_non_existed_station_name_then_returns_station_does_not_exist_and_none(self):
        createAStationBy(self.station_controller)

        status, station = self.station_controller.get_station_by_station_name(stationName=TEST_STATION_WRONG_STATION_NAME)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS_CODE, STATION_DOES_NOT_EXIST_DETAIL)
        assert station is None

    def test_given_a_station_is_created_when_creating_a_new_station_with_the_existed_station_name_then_returns_station_exist_and_none(self):
        createAStationBy(self.station_controller)

        status, station = self.station_controller.create_new_station(TEST_STATION_NAME, TEST_STATION_POSITION)

        assertStatus(status, STATION_EXIST_STATUS_CODE, STATION_EXIST_DETAIL)
        assert station is None

        _, stations = self.station_controller.get_all_stations()
        assert len(stations) == 1

    def test_given_a_station_is_created_when_querying_refresh_the_station_key_then_returns_ok_and_station(self):
        _, station = createAStationBy(self.station_controller)
        oldStationKey = station.stationKey

        status, new_station = self.station_controller.reset_station_key(TEST_STATION_NAME)

        assertStatus(status, HTTP_200_OK)
        assertStation(station, TEST_STATION_NAME, TEST_STATION_POSITION) 

        assert oldStationKey != new_station.stationKey

    def test_given_a_station_is_created_when_querying_refresh_the_station_key_of_non_existed_station_then_returns_statin_does_not_exist_and_none(self):
        createAStationBy(self.station_controller)

        status, station = self.station_controller.reset_station_key(TEST_STATION_WRONG_STATION_NAME)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS_CODE, STATION_DOES_NOT_EXIST_DETAIL)
        assert station is None

    def test_given_a_station_is_created_and_a_user_is_created_without_any_relationship_when_querying_all_stations_by_username_then_returns_ok_and_stations_array(self):
        creataAStationAndAnUserBy(self.user_controller, self.station_controller)

        status, stations = self.station_controller.get_station_by_username(username=FIRST_TEST_USER_USERNAME)

        assertStatus(status, HTTP_200_OK)
        self.assertListEqual(stations, [])

    def test_given_a_station_is_created_and_a_user_is_created_when_the_relationship_is_created_then_returns_ok_and_station(self):
        creataAStationAndAnUserBy(self.user_controller, self.station_controller)

        status, station = self.station_controller.add_username(username=FIRST_TEST_USER_USERNAME, stationName=TEST_STATION_NAME)

        assertStatus(status, HTTP_200_OK)
        assertStation(station, TEST_STATION_NAME, TEST_STATION_POSITION)

    def test_given_a_station_is_created_and_a_user_is_created_and_the_relationship_is_created_when_querying_all_stations_by_username_then_returns_ok_and_tthe_array_of_that_station(self):
        createAStationAndAnUserAndAddRelationshipBy(self.user_controller, self.station_controller)
        
        status, stations = self.station_controller.get_station_by_username(username=FIRST_TEST_USER_USERNAME)

        assertStatus(status, HTTP_200_OK)
        assert len(stations) == 1
        assertStation(stations[0], TEST_STATION_NAME, TEST_STATION_POSITION)

    def test_give_a_station_user_and_relationship_are_created_when_querying_all_stations_by_username_with_non_existed_username_then_returns_user_does_not_exist_and_none(self):
        createAStationAndAnUserAndAddRelationshipBy(self.user_controller, self.station_controller)

        status, stations = self.station_controller.get_station_by_username(username=FIRST_TEST_USER_USERNAME)

        assertStatus(status, USERNAME_DOES_NOT_EXISTED_STATUS_CODE, USERNAME_DOES_NOT_EXISTED_DETAIL)
        assert stations is None
