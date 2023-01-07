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
)
from tests import (
    get_testing_session,
)
from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
    HTTP_200_OK,
)
from tests.controllers import (
    assertStatus,
    assertStation,
)


class StationControllerTest(unittest.TestCase):
    test_station_name = "Ha Noi"
    test_station_position = "Dong Da, Ha Noi"

    def setUp(self):
        self.session = next(get_testing_session())
        self.station_controller = StationController(self.session)

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
