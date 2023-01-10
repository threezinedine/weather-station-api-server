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
    get_loggin_token,
    getAuthorizationHeader,
    FIRST_RECORD_TESTING,
    FIRST_WRONG_STATIONID_RECORD_TESTING,
    WRONG_STATION_KEY,
)
from app.constants import (
    STATION_STATION_KEY_KEY,
    WEATHER_DATA_KEY,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from app import (
    CREATE_RECORD_FULL_ROUTE,
    GET_THE_LATEST_RECORD_FULL_ROUTE,
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

        response = test_client.post(
            CREATE_RECORD_FULL_ROUTE,
            json={
                STATION_STATION_KEY_KEY: station.stationKey,
                WEATHER_DATA_KEY: FIRST_WRONG_STATIONID_RECORD_TESTING
            }
        )

        assert response.status_code == HTTP_404_NOT_FOUND

        response = test_client.post(
            CREATE_RECORD_FULL_ROUTE,
            json={
                STATION_STATION_KEY_KEY: WRONG_STATION_KEY,
                WEATHER_DATA_KEY: FIRST_RECORD_TESTING
            }
        )

        assert response.status_code == HTTP_400_BAD_REQUEST

    @unittest.skip("")
    def test_get_the_latest_record(self):
        _, station = createAStationAndAnUserAndAddRelationshipBy(self.user_controller, self.station_controller)
        self.record_controller.create_new_record(station.stationKey, **FIRST_RECORD_TESTING)

        token = get_loggin_token()

        response = test_client.get(
            f"/records/{station.stationName}/latest",
            headers=getAuthorizationHeader(token)
        )

        assert response == HTTP_200_OK
        assertRecord(response.json(), FIRST_RECORD_TESTING)
