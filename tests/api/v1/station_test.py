import unittest
import pytest
from fastapi.testclient import TestClient
from copy import copy

from main import app
from database.connection import get_session
from app.controllers import (
    UserController,
    StationController,
)
from app import (
    LOGIN_FULL_ROUTE,
    ALL_STATIONS_FULL_ROUTE,
    CREATE_A_STATION_FULL_ROUTE,
    ADD_NEW_STATION_FULL_ROUTE,
    RESET_STATION_KEY_FULL_ROUTE,
    GET_A_STATION_ROUTE,
    STATION_BASE_ROUTE,
)
from tests import (
    FIRST_TEST_USER_USERNAME,
    FIRST_TEST_USER_PASSWORD,
    FIRST_TEST_STATION_STATION_NAME,
    FIRST_TEST_STATION_STATION_POSITION,
    FIRST_TEST_STATION_WRONG_STATION_NAME,
    SECOND_TEST_STATION_STATION_NAME,
    SECOND_TEST_STATION_STATION_POSITION,
    WRONG_TOKEN,
    WRONG_STATION_KEY,
    clean_database,
    get_testing_session,
    createAnUserBy,
    createAStationBy,
    createTwoStationsBy,
    createAStationAndAnUserAndAddRelationshipBy,
    assertStation,
    assertStationDict,
    getAuthorizationHeader,
    test_client,
    get_loggin_token,
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
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from app.exceptions import (
    UNAUTHORIZATION_STATUS_CODE,
)


class StationTest(unittest.TestCase):
    def setUp(self):
        app.dependency_overrides[get_session] = get_testing_session
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)
        self.station_controller = StationController(self.session)

    def tearDown(self):
        clean_database(self.session)

    def test_create_station_feature(self):
        createAnUserBy(self.user_controller)
        token = get_loggin_token()

        response = test_client.post(
                    CREATE_A_STATION_FULL_ROUTE,
                    headers=getAuthorizationHeader(token),
                    json={
                        STATION_NAME_KEY: FIRST_TEST_STATION_STATION_NAME,
                        STATION_POSITION_KEY: FIRST_TEST_STATION_STATION_POSITION,
                    },
                )

        assert response.status_code == HTTP_200_OK
        _, stations = self.station_controller.get_station_by_username(FIRST_TEST_USER_USERNAME)
        assert len(stations) == 1
        assertStation(stations[0], FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

        response = test_client.post(
                    CREATE_A_STATION_FULL_ROUTE,
                    json={
                        STATION_NAME_KEY: FIRST_TEST_STATION_STATION_NAME,
                        STATION_POSITION_KEY: FIRST_TEST_STATION_STATION_POSITION,
                    },
                )

        assert response.status_code == UNAUTHORIZATION_STATUS_CODE
        _, stations = self.station_controller.get_station_by_username(FIRST_TEST_USER_USERNAME)
        assert len(stations) == 1

        response = test_client.post(
                CREATE_A_STATION_FULL_ROUTE,
                headers=getAuthorizationHeader(token),
                json={
                    STATION_NAME_KEY: FIRST_TEST_STATION_STATION_NAME,
                    STATION_POSITION_KEY: FIRST_TEST_STATION_STATION_POSITION,
                },
        )

    def test_add_station_via_station_key(self):
        createAnUserBy(self.user_controller)
        _, station = createAStationBy(self.station_controller)
        token = get_loggin_token()

        response = test_client.put(
                    ADD_NEW_STATION_FULL_ROUTE,
                    json={
                        STATION_STATION_KEY_KEY: WRONG_STATION_KEY,
                    }
                )

        assert response.status_code == HTTP_401_UNAUTHORIZED

        response = test_client.put(
                    ADD_NEW_STATION_FULL_ROUTE,
                    headers=getAuthorizationHeader(token),
                    json={
                        STATION_STATION_KEY_KEY: WRONG_STATION_KEY,
                    }
                )

        assert response.status_code == HTTP_404_NOT_FOUND

        response = test_client.put(
                    ADD_NEW_STATION_FULL_ROUTE,
                    headers=getAuthorizationHeader(token),
                    json={
                        STATION_STATION_KEY_KEY: station.stationKey,
                    }
                )

        assert response.status_code == HTTP_200_OK

        _, stations = self.station_controller.get_station_by_username(FIRST_TEST_USER_USERNAME)
        assert len(stations) == 1
        assertStation(stations[0], FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

    def test_reset_station_key_feature(self):
        _, station = createAStationAndAnUserAndAddRelationshipBy(self.user_controller, self.station_controller)
        stationKey = copy(station.stationKey)
        token = get_loggin_token()

        response = test_client.put(
                    RESET_STATION_KEY_FULL_ROUTE,
                    json={
                        STATION_NAME_KEY: FIRST_TEST_STATION_STATION_NAME
                    }
                )

        response = test_client.put(
                    RESET_STATION_KEY_FULL_ROUTE,
                    headers=getAuthorizationHeader(token),
                    json={
                        STATION_NAME_KEY: FIRST_TEST_STATION_WRONG_STATION_NAME
                    }
                )

        assert response.status_code == HTTP_404_NOT_FOUND

        response = test_client.put(
                    RESET_STATION_KEY_FULL_ROUTE,
                    headers=getAuthorizationHeader(token),
                    json={
                        STATION_NAME_KEY: FIRST_TEST_STATION_STATION_NAME,
                    }
                )

        assert response.status_code == HTTP_200_OK
        assert response.json()[STATION_STATION_KEY_KEY] != stationKey

        _, stations = self.station_controller.get_station_by_username(FIRST_TEST_USER_USERNAME)
        assert stations[0]


    def test_get_all_stations_feature(self):
        createAnUserBy(self.user_controller)
        createTwoStationsBy(self.station_controller)

        self.station_controller.add_username(username=FIRST_TEST_USER_USERNAME, stationName=FIRST_TEST_STATION_STATION_NAME)
        token = get_loggin_token()

        response = test_client.get(
                ALL_STATIONS_FULL_ROUTE, 
                headers=getAuthorizationHeader(token)
            )

        assert response.status_code == HTTP_200_OK
        assert len(response.json()) == 1
        stations = response.json()

        assertStationDict(stations[0], FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)


        self.station_controller.add_username(username=FIRST_TEST_USER_USERNAME, stationName=SECOND_TEST_STATION_STATION_NAME)

        response = test_client.get(
                ALL_STATIONS_FULL_ROUTE, 
                headers=getAuthorizationHeader(token)
            )

        assert response.status_code == HTTP_200_OK
        assert len(response.json()) == 2
        stations = response.json()

        assertStationDict(stations[0], FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)
        assertStationDict(stations[1], SECOND_TEST_STATION_STATION_NAME, SECOND_TEST_STATION_STATION_POSITION)


        response = test_client.get(
                ALL_STATIONS_FULL_ROUTE, 
            )

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_get_a_station_feature(self):
        GET_FIRST_TEST_STATION_FULL_ROUTE = f"{STATION_BASE_ROUTE}/{FIRST_TEST_STATION_STATION_NAME}"
        GET_FIRST_TEST_WRONG_STATION_FULL_ROUTE = f"{STATION_BASE_ROUTE}/{FIRST_TEST_STATION_WRONG_STATION_NAME}"

        createAnUserBy(self.user_controller)
        createTwoStationsBy(self.station_controller)

        self.station_controller.add_username(username=FIRST_TEST_USER_USERNAME, stationName=FIRST_TEST_STATION_STATION_NAME)
        token = get_loggin_token()

        response = test_client.get(
                    GET_FIRST_TEST_STATION_FULL_ROUTE,
                    headers=getAuthorizationHeader(token)
                )

        assert response.status_code == HTTP_200_OK
        assertStationDict(response.json(), FIRST_TEST_STATION_STATION_NAME, FIRST_TEST_STATION_STATION_POSITION)

        response = test_client.get(
                    GET_FIRST_TEST_STATION_FULL_ROUTE,
                )

        assert response.status_code == HTTP_401_UNAUTHORIZED


        response = test_client.get(
                    GET_FIRST_TEST_WRONG_STATION_FULL_ROUTE,
                    headers=getAuthorizationHeader(token)
                )

        assert response.status_code == HTTP_404_NOT_FOUND
