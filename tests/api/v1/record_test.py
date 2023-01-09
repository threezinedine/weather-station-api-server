import unittest

from app.controllers import (
    UserController,
    StationController,
    RecordController,
)
from tests import (
    test_client,
    clean_database,
    get_testing_session,
    createAStationAndAnUserAndAddRelationshipBy,
    assertRecord,
    FIRST_RECORD_TESTING,
)
from app.constants import (
    STATION_STATION_KEY_KEY,
    WEATHER_DATA_KEY,
    HTTP_200_OK,
)
from app import (
    CREATE_RECORD_FULL_ROUTE,
)


class RecordTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)
        self.station_controller = StationController(self.session)
        self.record_controller = RecordController(self.session)

    def tearDown(self):
        clean_database(self.session)

    def test_create_a_record(self):
        _, station = createAStationAndAnUserAndAddRelationshipBy(self.user_controller, self.station_controller)

        response = test_client.post(
                CREATE_RECORD_FULL_ROUTE,
                json={
                    STATION_STATION_KEY_KEY: station.stationKey,
                    WEATHER_DATA_KEY: FIRST_RECORD_TESTING,
                }
            )

        assert response.status_code == HTTP_200_OK

        _, records = self.record_controller.get_all_records()
        assert len(records) == 1
        assertRecord(records[0], FIRST_RECORD_TESTING)
