import unittest
import pytest
from fastapi.testclient import TestClient

from main import app
from database.connection import get_session
from app.controllers import (
    UserController,
    StationController,
)
from app import (
    LOGIN_FULL_ROUTE,
    CREATE_A_STATION_FULL_ROUTE,
    ADD_NEW_STATION_FULL_ROUTE,
)
from tests import (
    FIRST_TEST_USER_USERNAME,
    FIRST_TEST_USER_PASSWORD,
    FIRST_TEST_STATION_STATION_NAME,
    FIRST_TEST_STATION_STATION_POSITION,
    WRONG_TOKEN,
    clean_database,
    get_testing_session,
    createAnUserBy,
    createAStationBy,
    assertStation,
    get_sent_token,
)
from app.constants import (
    USERNAME_KEY,
    PASSWORD_KEY,
    USERID_KEY,
    TOKEN_KEY,
    AUTHORIZATION_KEY,
    STATION_NAME_KEY,
    STATION_POSITION_KEY,
    STATION_STATION_KEY_KEY,
    PUSHING_DATA_INTERVAL_IN_SECONDS_KEY,
)
from app.constants import (
    HTTP_200_OK,
)
from app.exceptions import (
    UNAUTHORIZATION_STATUS_CODE,
)


class StationTest(unittest.TestCase):
    def setUp(self):
        app.dependency_overrides[get_session] = get_testing_session
        self.test_client = TestClient(app)
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)
        self.station_controller = StationController(self.session)

    def tearDown(self):
        clean_database(self.session)

    def test_create_station_feature(self):
        createAnUserBy(self.user_controller)

        login_response = self.test_client.post(
                    LOGIN_FULL_ROUTE,
                    json={
                        USERNAME_KEY: FIRST_TEST_USER_USERNAME,
                        PASSWORD_KEY: FIRST_TEST_USER_PASSWORD, 
                    }
                )

        token = login_response.json()[TOKEN_KEY]

        response = self.test_client.post(
                    CREATE_A_STATION_FULL_ROUTE,
                    headers={
                        AUTHORIZATION_KEY: get_sent_token(token) 
                    },
                    json={
                        STATION_NAME_KEY: FIRST_TEST_STATION_STATION_NAME,
                        STATION_POSITION_KEY: FIRST_TEST_STATION_STATION_POSITION,
                    },
                )

        assert response.status_code == HTTP_200_OK
        _, stations = self.station_controller.get_station_by_username(FIRST_TEST_USER_USERNAME)
        assert len(stations) == 1
        assertStation(stations[0], FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

        response = self.test_client.post(
                    CREATE_A_STATION_FULL_ROUTE,
                    json={
                        STATION_NAME_KEY: FIRST_TEST_STATION_STATION_NAME,
                        STATION_POSITION_KEY: FIRST_TEST_STATION_STATION_POSITION,
                    },
                )

        assert response.status_code == UNAUTHORIZATION_STATUS_CODE
        _, stations = self.station_controller.get_station_by_username(FIRST_TEST_USER_USERNAME)
        assert len(stations) == 1

        response = self.test_client.post(
                CREATE_A_STATION_FULL_ROUTE,
                headers={
                    AUTHORIZATION_KEY: get_sent_token(WRONG_TOKEN)
                },
                json={
                    STATION_NAME_KEY: FIRST_TEST_STATION_STATION_NAME,
                    STATION_POSITION_KEY: FIRST_TEST_STATION_STATION_POSITION,
                },
        )

    def test_add_station_via_station_key(self):
        createAnUserBy(self.user_controller)
        _, station = createAStationBy(self.station_controller)

        login_response = self.test_client.post(
                    LOGIN_FULL_ROUTE,
                    json={
                        USERNAME_KEY: FIRST_TEST_USER_USERNAME,
                        PASSWORD_KEY: FIRST_TEST_USER_PASSWORD, 
                    }
                )

        token = login_response.json()[TOKEN_KEY]

        response = self.test_client.put(
                    ADD_NEW_STATION_FULL_ROUTE,
                    headers={
                        AUTHORIZATION_KEY: get_sent_token(token)
                    },
                    json={
                        STATION_STATION_KEY_KEY: station.stationKey,
                    }
                )

        assert response.status_code == HTTP_200_OK

        _, stations = self.station_controller.get_station_by_username(FIRST_TEST_USER_USERNAME)
        assert len(stations) == 1
        assertStation(stations[0], FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)
