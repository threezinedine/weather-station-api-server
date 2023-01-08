import unittest

from tests.controllers import (
    get_testing_session,
    clean_database,
    assertStatus,
    assertRecord,
    OK_STATUS,
    createAStationBy,
    FIRST_RECORD_TESTING,
    FIRST_STATION_WRONG_STATION_KEY,
    FIRST_TEST_STATION_STATION_NAME,
    createAStationWithExampleRecordBy,
)
from app.controllers import (
    RecordController,
    StationController,
)
from app.exceptions import (
    WRONG_STATION_KEY_STATUS,
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

    def test_given_a_station_is_created_when_creating_a_new_record_then_returns_ok_and_that_record(self):
        _, station = createAStationBy(self.station_controller)

        status, record = self.record_controller.create_new_record(stationKey=station.stationKey, **FIRST_RECORD_TESTING)

        assertStatus(status, OK_STATUS)
        assertRecord(record, FIRST_RECORD_TESTING)

    def test_given_a_station_and_a_record_are_created_when_querying_all_records_then_returns_ok_and_the_list_that_contains_that_record(self):
        createAStationWithExampleRecordBy(self.station_controller, self.record_controller)

        status, records = self.record_controller.get_all_records()

        assertStatus(status, OK_STATUS)
        assert len(records) == 1
        assertRecord(records[0], FIRST_RECORD_TESTING)

    def test_given_a_station_is_created_when_creating_a_new_record_with_invalid_station_key_then_returns_wrong_station_key_and_none(self):
        createAStationBy(self.station_controller)

        status, record = self.record_controller.create_new_record(stationKey=FIRST_STATION_WRONG_STATION_KEY, **FIRST_RECORD_TESTING)
        
        assertStatus(status, WRONG_STATION_KEY_STATUS)
        assert record is None
        _, records = self.record_controller.get_all_records()
        self.assertListEqual(records, [])

    def test_given_a_station_and_a_record_are_created_when_querying_all_records_from_the_existed_station_then_returns_ok_and_list_of_records(self):
        createAStationWithExampleRecordBy(self.station_controller, self.record_controller)

        status, records = self.record_controller.get_all_records_from_station(stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, OK_STATUS)
        assert len(records) == 1
        assertRecord(records[0], FIRST_RECORD_TESTING)
