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
    FIRST_TEST_STATION_WRONG_STATION_NAME,
    FIRST_TEST_STATION_STATION_NAME,
    FIRST_WRONG_STATIONID_RECORD_TESTING,
    SECOND_RECORD_TESTING,
    createAStationBy,
    createAStationWithExampleRecordBy,
    createAStationWithTwoExampleRecordsBy,
)
from app.controllers import (
    RecordController,
    StationController,
)
from app.exceptions import (
    WRONG_STATION_KEY_STATUS,
    STATION_DOES_NOT_EXIST_STATUS,
    NO_RECORD_EXIST_STATUS,
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

    def test_given_a_station_is_created_when_creating_a_new_record_with_non_existed_station_then_returns_station_does_not_exist_and_none(self):
        createAStationBy(self.station_controller)

        status, record = self.record_controller.create_new_record(stationKey=FIRST_STATION_WRONG_STATION_KEY, **FIRST_WRONG_STATIONID_RECORD_TESTING)

    def test_given_a_station_and_a_record_are_created_when_querying_all_records_from_the_existed_station_then_returns_ok_and_list_of_records(self):
        createAStationWithExampleRecordBy(self.station_controller, self.record_controller)

        status, records = self.record_controller.get_all_records_from_station(stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, OK_STATUS)
        assert len(records) == 1
        assertRecord(records[0], FIRST_RECORD_TESTING)

    def test_given_a_station_and_a_record_are_created_when_querying_all_records_of_non_existed_station_then_returns_station_does_not_exist_and_none(self):
        createAStationWithExampleRecordBy(self.station_controller, self.record_controller)

        status, records = self.record_controller.get_all_records_from_station(stationName=FIRST_TEST_STATION_WRONG_STATION_NAME)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS)
        assert records is None

    def test_given_a_station_and_two_record_are_created_when_querying_the_lastest_record_of_existed_station_then_returns_ok_and_record(self):
        createAStationWithTwoExampleRecordsBy(self.station_controller, self.record_controller)

        status, record = self.record_controller.get_latest_record_from_station(stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, OK_STATUS)
        assertRecord(record, SECOND_RECORD_TESTING) 

    def test_given_a_station_and_a_record_are_created_when_querying_the_latest_record_of_non_existed_station_then_returns_station_does_not_exist_and_none(self):
        createAStationWithExampleRecordBy(self.station_controller, self.record_controller)

        status, record = self.record_controller.get_latest_record_from_station(stationName=FIRST_TEST_STATION_WRONG_STATION_NAME)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS)
        assert record is None

    def test_given_a_station_is_created_when_querying_the_latest_record_of_this_station_then_returns_no_record_exists_and_none(self):
        createAStationBy(self.station_controller)

        status, record = self.record_controller.get_latest_record_from_station(stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, NO_RECORD_EXIST_STATUS)
        assert record is None

    def test_given_a_station_and_two_records_are_created_when_deleting_all_the_records_from_that_station_then_return_ok_and_none(self):
        createAStationWithTwoExampleRecordsBy(self.station_controller, self.record_controller)

        status, record = self.record_controller.delete_all_records_by_station_name(stationName=FIRST_TEST_STATION_STATION_NAME)

        assertStatus(status, OK_STATUS)
        assert record is None

        _, records = self.record_controller.get_all_records_from_station(stationName=FIRST_TEST_STATION_STATION_NAME)
        self.assertListEqual(records, [])

    def test_given_a_staiton_and_two_records_are_created_when_deleting_all_records_from_non_existed_station_then_returns_station_does_not_exist_and_none(self):
        createAStationWithTwoExampleRecordsBy(self.station_controller, self.record_controller)
        
        status, record = self.record_controller.delete_all_records_by_station_name(stationName=FIRST_TEST_STATION_WRONG_STATION_NAME)

        assertStatus(status, STATION_DOES_NOT_EXIST_STATUS)
        assert record is None
