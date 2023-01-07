import unittest
from typing import (
    Dict,
    Union,
)

from database.models import (
    User,
    Station,
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
)
from tests.controllers import (
    assertStatus,
    assertStation,
)


class StationControllerTest(unittest.TestCase):
    test_station_name = "Ha Noi"
    test_station_position = "Dong Da, Ha Noi"
    wrong_testing_station_name = "HA Noi"

    def setUp(self):
        self.session = next(get_testing_session())
        self.station_controller = StationController(self.session)
        self.user_controller = UserController(self.session)

    def tearDown(self):
        self.session.query(User).delete()
        self.session.query(Station).delete()
        self.session.commit()
        self.session.close()

    def assertStation(self, station: Station, stationName: str, stationPosition: str, pushingDataIntervalInSeconds: int = 5):
        assert station.stationName == stationName
        assert station.stationPosition == stationPosition
        assert station.pushingDataIntervalInSeconds == pushingDataIntervalInSeconds

    def test_given_no_station_is_created_when_querying_all_stations_then_returns_ok_and_empty_array(self):
        status, stations = self.station_controller.get_all_stations()

        assertStatus(status, HTTP_200_OK)
        self.assertListEqual(stations, [])

    def test_given_no_station_is_created_when_creating_new_station_then_returns_ok_and_that_station(self):
        status, station = self.station_controller.create_new_station(stationName=self.test_station_name, stationPosition=self.test_station_position)

        assertStatus(status, HTTP_200_OK)
        assertStation(station, self.test_station_name, self.test_station_position)

    def test_given_a_station_is_created_when_querying_all_stations_then_returns_ok_and_station_list(self):
        self.station_controller.create_new_station(self.test_station_name, self.test_station_position)

        status, stations = self.station_controller.get_all_stations()

        assertStatus(status, HTTP_200_OK)
        assert len(stations) == 1
        assertStation(stations[0], self.test_station_name, self.test_station_position)

    def test_given_a_station_is_created_when_querying_station_by_valid_station_name_then_returns_ok_and_station(self):
        self.station_controller.create_new_station(self.test_station_name, self.test_station_position)

        status, station = self.station_controller.get_station_by_station_name(stationName=self.test_station_name)

        assertStatus(status, HTTP_200_OK)
        assertStation(station, self.test_station_name, self.test_station_position)

    def test_given_a_station_is_created_when_querying_station_by_non_existed_station_name_then_returns_station_does_not_exist_and_none(self):
        self.station_controller.create_new_station(self.test_station_name, self.test_station_position)

        status, station = self.station_controller.get_station_by_station_name(stationName=self.wrong_testing_station_name)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS_CODE, STATION_DOES_NOT_EXIST_DETAIL)
        assert station is None

    def test_given_a_station_is_created_when_creating_a_new_station_with_the_existed_station_name_then_returns_station_exist_and_none(self):
        self.station_controller.create_new_station(self.test_station_name, self.test_station_position)

        status, station = self.station_controller.create_new_station(self.test_station_name, self.test_station_position)

        assertStatus(status, 409, "The station exists.")
        assert station is None

        _, stations = self.station_controller.get_all_stations()
        assert len(stations) == 1

    def test_given_a_station_is_created_when_querying_refresh_the_station_key_then_returns_ok_and_station(self):
        _, station = self.station_controller.create_new_station(self.test_station_name, self.test_station_position)
        oldStationKey = station.stationKey

        status, new_station = self.station_controller.reset_station_key(self.test_station_name)

        assertStatus(status, HTTP_200_OK)
        assertStation(station, self.test_station_name, self.test_station_position) 

        assert oldStationKey != new_station.stationKey

    def test_given_a_station_is_created_when_querying_refresh_the_station_key_of_non_existed_station_then_returns_statin_does_not_exist_and_none(self):
        self.station_controller.create_new_station(self.test_station_name, self.test_station_position)

        status, station = self.station_controller.reset_station_key(self.wrong_testing_station_name)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS_CODE, STATION_DOES_NOT_EXIST_DETAIL)
        assert station is None

    def test_given_a_station_is_created_and_a_user_is_created_without_any_relationship_when_querying_all_stations_by_username_then_returns_ok_and_stations_array(self):
        self.station_controller.create_new_station(self.test_station_name, self.test_station_position)
        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

        status, stations = self.station_controller.get_station_by_username(username="threezinedine")

        assertStatus(status, HTTP_200_OK)
        self.assertListEqual(stations, [])

    def test_given_a_station_is_created_and_a_user_is_created_when_the_relationship_is_created_then_returns_ok_and_station(self):
        self.station_controller.create_new_station(self.test_station_name, self.test_station_position)
        self.user_controller.create_new_user(username="threezinedine", password="threezinedine")

        status, station = self.station_controller.add_username(username="threezinedine", stationName=self.test_station_name)

        assertStatus(status, HTTP_200_OK)
        assertStation(station, self.test_station_name, self.test_station_position)
