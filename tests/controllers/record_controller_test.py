import unittest

from tests.controllers import (
    get_testing_session,
    clean_database,
    assertStatus,
    OK_STATUS,
    createAStationBy,
)
from app.controllers import (
    RecordController,
    StationController,
)


FIRST_RECORD_TESTING = dict(stationId=1,
                                windDirection=1,
                                averageWindSpeedInOneMinute=2.3,
                                maxWindSpeedInFiveMinutes=3.4,
                                rainFallInOneHour=23.1,
                                rainFallInOneDay=13.2,
                                temperature=34.23,
                                humidity=23,
                                barPressure=-123.00,
                                createdTime="2023-01-08"
                                )


class RecordControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session()) 
        self.record_controller = RecordController(self.session)
        self.station_controller = StationController(self.session)

    def tearDown(self):
        clean_database(self.session)

    def test_given_no_record_is_created_when_querying_all_records_then_returns_ok_and_an_empty_array(self):
        status, records = self.record_controller.get_all_records()

        assertStatus(status, OK_STATUS)
        self.assertListEqual(records, [])

    def test_given_a_station_is_created_then_creating_a_new_record_then_returns_ok_and_that_record(self):
        createAStationBy(self.station_controller)

        status, record = self.record_controller.create_a_new_record(**FIRST_RECORD_TESTING)

        assertStatus(status, OK_STATUS)
        assertRecord(record, FIRST_RECORD_TESTING)
