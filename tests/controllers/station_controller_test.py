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


class StationControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.station_controller = StationController(self.session)

    def tearDown(self):
        self.session.query(User).delete()
        self.session.query(Station).delete()
        self.session.commit()
        self.session.close()

    def test_given_no_station_is_created_when_querying_all_stations_then_returns_ok_and_empty_array(self):
        status, stations = self.station_controller.get_all_stations()

        assert status[STATUS_CODE_KEY] == HTTP_200_OK
        assert status[DETAIL_KEY] is None

        self.assertListEqual(stations, [])

    def test_given_no_station_is_created_when_creating_new_station_then_returns_ok_and_that_station(self):
        status, station = self.station_controller.create_new_station(stationName="Ha Noi", stationPosition="Ha Noi")

        assert status[STATUS_CODE_KEY] == HTTP_200_OK
        assert status[DETAIL_KEY] is None

        assert station.stationName == "Ha Noi"
        assert station.stationPosition == "Ha Noi"
