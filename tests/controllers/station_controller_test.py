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
from app.exceptions import (
    OK_STATUS,
    STATION_DOES_NOT_EXIST_STATUS,
    STATION_EXIST_STATUS,
    USER_DOES_NOT_EXIST_STATUS,
    NO_RELATIONSHIP_EXIST_STATUS,
)
from tests import (
    get_testing_session,
    assertStatus,
    assertStation,
    FIRST_TEST_STATION_STATION_NAME,
    FIRST_TEST_STATION_STATION_POSITION,
    FIRST_TEST_STATION_WRONG_STATION_NAME,
    TEST_STATION_DEFAULT_PUSHING_DATA_INTERVAL_IN_SECONDS,
    TEST_STATION_PUSHING_DATA_INTERVAL_IN_SECONDS,
    SECOND_TEST_STATION_STATION_NAME,
    SECOND_TEST_STATION_STATION_POSITION,
    FIRST_TEST_USER_USERNAME,
    FIRST_TEST_USER_PASSWORD,
    FIRST_TEST_USER_WRONG_USERNAME,
    createAStationBy,
    createTwoStationsBy,
    creataAStationAndAnUserBy,
    createAStationAndAnUserAndAddRelationshipBy,
    clean_database,
)


class StationControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.station_controller = StationController(self.session)
        self.user_controller = UserController(self.session)

    def tearDown(self):
        clean_database(self.session)

    def assertStation(self, station: Station, stationName: str, 
            stationPosition: str, pushingDataIntervalInSeconds: int = TEST_STATION_DEFAULT_PUSHING_DATA_INTERVAL_IN_SECONDS):
        assert station.stationName == stationName
        assert station.stationPosition == stationPosition
        assert station.pushingDataIntervalInSeconds == pushingDataIntervalInSeconds

    def test_given_no_station_is_created_when_querying_all_stations_then_returns_ok_and_empty_array(self):
        status, stations = self.station_controller.get_all_stations()

        assertStatus(status, OK_STATUS)
        self.assertListEqual(stations, [])

    def test_given_no_station_is_created_when_creating_new_station_then_returns_ok_and_that_station(self):
        status, station = self.station_controller.create_new_station(stationName=FIRST_TEST_STATION_STATION_NAME, stationPosition=FIRST_TEST_STATION_STATION_POSITION)

        assertStatus(status, OK_STATUS)
        assertStation(station, FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

    def test_given_a_station_is_created_when_querying_all_stations_then_returns_ok_and_station_list(self):
        createAStationBy(self.station_controller)

        status, stations = self.station_controller.get_all_stations()

        assertStatus(status, OK_STATUS)
        assert len(stations) == 1
        assertStation(stations[0], FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

    def test_given_a_station_is_created_when_querying_station_by_valid_station_name_then_returns_ok_and_station(self):
        createAStationBy(self.station_controller)

        status, station = self.station_controller.get_station_by_station_name(stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, OK_STATUS)
        assertStation(station, FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

    def test_given_a_station_is_created_when_querying_station_by_non_existed_station_name_then_returns_station_does_not_exist_and_none(self):
        createAStationBy(self.station_controller)

        status, station = self.station_controller.get_station_by_station_name(stationName=FIRST_TEST_STATION_WRONG_STATION_NAME)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS)
        assert station is None

    def test_given_a_station_is_created_when_creating_a_new_station_with_the_existed_station_name_then_returns_station_exist_and_none(self):
        createAStationBy(self.station_controller)

        status, station = self.station_controller.create_new_station(FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

        assertStatus(status, STATION_EXIST_STATUS)
        assert station is None

        _, stations = self.station_controller.get_all_stations()
        assert len(stations) == 1

    def test_given_a_station_is_created_when_querying_refresh_the_station_key_then_returns_ok_and_station(self):
        _, station = createAStationBy(self.station_controller)
        oldStationKey = station.stationKey

        status, new_station = self.station_controller.reset_station_key(FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, OK_STATUS)
        assertStation(station, FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION) 

        assert oldStationKey != new_station.stationKey

    def test_given_a_station_is_created_when_querying_refresh_the_station_key_of_non_existed_station_then_returns_statin_does_not_exist_and_none(self):
        createAStationBy(self.station_controller)

        status, station = self.station_controller.reset_station_key(FIRST_TEST_STATION_WRONG_STATION_NAME)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS)
        assert station is None

    def test_given_a_station_is_created_and_a_user_is_created_without_any_relationship_when_querying_all_stations_by_username_then_returns_ok_and_stations_array(self):
        creataAStationAndAnUserBy(self.user_controller, self.station_controller)

        status, stations = self.station_controller.get_station_by_username(username=FIRST_TEST_USER_USERNAME)

        assertStatus(status, OK_STATUS)
        self.assertListEqual(stations, [])

    def test_given_a_station_is_created_and_a_user_is_created_when_the_relationship_is_created_then_returns_ok_and_station(self):
        creataAStationAndAnUserBy(self.user_controller, self.station_controller)

        status, station = self.station_controller.add_username(username=FIRST_TEST_USER_USERNAME, stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, OK_STATUS)
        assertStation(station, FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

    def test_given_a_station_is_created_and_a_user_is_created_and_the_relationship_is_created_when_querying_all_stations_by_username_then_returns_ok_and_tthe_array_of_that_station(self):
        createAStationAndAnUserAndAddRelationshipBy(self.user_controller, self.station_controller)
        
        status, stations = self.station_controller.get_station_by_username(username=FIRST_TEST_USER_USERNAME)

        assertStatus(status, OK_STATUS)
        assert len(stations) == 1
        assertStation(stations[0], FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

    def test_given_a_station_user_and_relationship_are_created_when_querying_all_stations_by_username_with_non_existed_username_then_returns_user_does_not_exist_and_none(self):
        createAStationAndAnUserAndAddRelationshipBy(self.user_controller, self.station_controller)

        status, stations = self.station_controller.get_station_by_username(username=FIRST_TEST_USER_WRONG_USERNAME)

        assertStatus(status, USER_DOES_NOT_EXIST_STATUS)
        assert stations is None

    def test_given_a_station_user_are_created_when_create_the_relationship_with_non_existed_username_then_returns_user_does_not_exist_and_none(self):
        creataAStationAndAnUserBy(self.user_controller, self.station_controller)

        status, station = self.station_controller.add_username(username=FIRST_TEST_USER_WRONG_USERNAME, stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, USER_DOES_NOT_EXIST_STATUS)
        assert station is None

    def test_given_a_station_user_are_created_when_create_the_relationship_with_non_existed_station_name_then_returns_station_does_not_exist_and_none(self):
        creataAStationAndAnUserBy(self.user_controller, self.station_controller)

        status, station = self.station_controller.add_username(username=FIRST_TEST_USER_USERNAME, stationName=FIRST_TEST_STATION_WRONG_STATION_NAME)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS)
        assert station is None

    def test_given_a_station_is_created_when_changing_the_pushing_interval_with_existed_station_then_returns_ok_and_that_station(self):
        createAStationBy(self.station_controller)

        status, station = self.station_controller.change_pushing_time_interval_in_seconds(stationName=FIRST_TEST_STATION_STATION_NAME, new_pushingDataIntervalInSeconds=TEST_STATION_PUSHING_DATA_INTERVAL_IN_SECONDS)
        
        assertStatus(status, OK_STATUS)
        assertStation(station, FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION, TEST_STATION_PUSHING_DATA_INTERVAL_IN_SECONDS)

        _, station = self.station_controller.get_station_by_station_name(FIRST_TEST_STATION_STATION_NAME)
        assertStation(station, FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION, TEST_STATION_PUSHING_DATA_INTERVAL_IN_SECONDS)

    def test_given_a_station_is_created_when_changing_the_pushing_interval_with_non_existed_station_return_retuns_station_does_not_exist_and_none(self):
        createAStationBy(self.station_controller)

        status, station = self.station_controller.change_pushing_time_interval_in_seconds(FIRST_TEST_STATION_WRONG_STATION_NAME, TEST_STATION_PUSHING_DATA_INTERVAL_IN_SECONDS)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS)
        assert station is None

    def test_given_two_stations_are_created_when_deleting_a_station_then_return_ok_and_none(self):
        createTwoStationsBy(self.station_controller)

        status, station = self.station_controller.delete_by_station_name(stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, OK_STATUS)
        assert station is None

        _, stations = self.station_controller.get_all_stations()
        assert len(stations) == 1
        assertStation(stations[0], SECOND_TEST_STATION_STATION_NAME, SECOND_TEST_STATION_STATION_POSITION)

    def test_given_a_station_is_created_when_deleting_a_non_existed_station_then_returns_station_does_not_exist_and_none(self):
        createAStationBy(self.station_controller)

        status, station = self.station_controller.delete_by_station_name(FIRST_TEST_STATION_WRONG_STATION_NAME)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS)
        assert station is None
        
        _, stations = self.station_controller.get_all_stations()
        assert len(stations) == 1
        assertStation(stations[0], FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

    def test_given_a_station_user_relationship_are_created_when_deleting_a_relationship_by_valid_username_then_return_ok_and_none(self):
        createAStationAndAnUserAndAddRelationshipBy(self.user_controller, self.station_controller)

        status, station = self.station_controller.delete_relationship(username=FIRST_TEST_USER_USERNAME, stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, OK_STATUS)
        assert station is None

        _, stations = self.station_controller.get_station_by_username(username=FIRST_TEST_USER_USERNAME)
        self.assertListEqual(stations, [])
        _, stations = self.station_controller.get_all_stations()
        assert len(stations) == 1

    def test_given_a_station_user_relationship_are_created_when_deleting_a_relationship_by_non_existed_user_then_returns_user_does_not_exist_and_none(self):
        createAStationAndAnUserAndAddRelationshipBy(self.user_controller, self.station_controller)

        status, station = self.station_controller.delete_relationship(username=FIRST_TEST_USER_WRONG_USERNAME, stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, USER_DOES_NOT_EXIST_STATUS)
        assert station is None
        
        _, stations = self.station_controller.get_station_by_username(username=FIRST_TEST_USER_USERNAME)
        assert len(stations) == 1
        assertStation(stations[0], FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

    def test_given_a_station_user_relationship_are_created_when_deleting_a_relationship_of_non_existed_station_then_return_station_does_not_exist_and_none(self):
        createAStationAndAnUserAndAddRelationshipBy(self.user_controller, self.station_controller)

        status, station = self.station_controller.delete_relationship(username=FIRST_TEST_USER_USERNAME, stationName=FIRST_TEST_STATION_WRONG_STATION_NAME)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS)
        assert station is None

    def test_given_a_station_user_are_created_when_deleting_the_relationship_between_them_then_returns_no_relationship_exists_and_none(self):
        creataAStationAndAnUserBy(self.user_controller, self.station_controller)

        status, station = self.station_controller.delete_relationship(username=FIRST_TEST_USER_USERNAME, stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, NO_RELATIONSHIP_EXIST_STATUS)
        assert station is None

    def test_given_a_user_and_station_are_created_when_add_the_username_by_valid_station_key_then_returns_ok_and_station(self):
        _, station = creataAStationAndAnUserBy(self.user_controller, self.station_controller)

        status, station = self.station_controller.add_username_with_station_key(username=FIRST_TEST_USER_USERNAME, stationKey=station.stationKey)

        assertStatus(status, OK_STATUS)
        assertStation(station, FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

        _, stations = self.station_controller.get_station_by_username(username=FIRST_TEST_USER_USERNAME)
        assert len(stations) == 1
