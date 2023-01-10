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
    createARecordAStationAndTwoUserBy,
    assertRecord,
    assertRecordDict,
    get_loggin_token,
    get_loggin_token_user_2,
    getAuthorizationHeader,
    FIRST_RECORD_TESTING,
    FIRST_WRONG_STATIONID_RECORD_TESTING,
    FIRST_TEST_STATION_WRONG_STATION_NAME,
    FIRST_TEST_STATION_STATION_NAME,
    WRONG_STATION_KEY,
)
from app.constants import (
    STATION_STATION_KEY_KEY,
    WEATHER_DATA_KEY,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
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

    def test_get_the_latest_record(self):
        createARecordAStationAndTwoUserBy(self.user_controller, self.station_controller, self.record_controller)

        route = f"/records/{FIRST_TEST_STATION_STATION_NAME}/latest"
        wrong_route = f"/records/{FIRST_TEST_STATION_WRONG_STATION_NAME}/latest"

        token = get_loggin_token()
        token_2 = get_loggin_token_user_2()

        response = test_client.get(
            route, 
            headers=getAuthorizationHeader(token)
        )

        assert response.status_code == HTTP_200_OK
        assertRecordDict(response.json(), FIRST_RECORD_TESTING)


        response = test_client.get(
            route,
            headers=getAuthorizationHeader(token_2)
        )

        assert response.status_code == HTTP_401_UNAUTHORIZED


        response = test_client.get(
            wrong_route,
            headers=getAuthorizationHeader(token)
        )

        assert response.status_code == HTTP_404_NOT_FOUND


        response = test_client.get(
            route,
        )

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_get_all_records(self):
        createARecordAStationAndTwoUserBy(self.user_controller, self.station_controller, self.record_controller)

        route = f"/records/{FIRST_TEST_STATION_STATION_NAME}/"
        wrong_route = f"/records/{FIRST_TEST_STATION_WRONG_STATION_NAME}/"

        token = get_loggin_token()
        token_2 = get_loggin_token_user_2()

        response = test_client.get(
            route,    
            headers=getAuthorizationHeader(token)
        )

        assert response.status_code == HTTP_200_OK
        assertRecordDict(response.json()[0], FIRST_RECORD_TESTING)
