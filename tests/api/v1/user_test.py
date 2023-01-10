import unittest
from fastapi.testclient import TestClient

from tests import (
    get_testing_session,
    clean_database,
    createAnUserBy,
    FIRST_TEST_USER_USERNAME,
    FIRST_TEST_USER_PASSWORD,
    FIRST_TEST_USER_WRONG_USERNAME,
    FIRST_TEST_USER_NEW_PASSWORD,
    test_client,
)
from app.constants import (
    USERNAME_KEY,
    PASSWORD_KEY,
    USER_KEY,
    TOKEN_KEY,
    USERID_KEY,
)
from app import (
    LOGIN_FULL_ROUTE,
    REGISTER_FULL_ROUTE,
)
from app.controllers import UserController
from app.exceptions import (
    HTTP_200_OK,
    USER_DOES_NOT_EXIST_STATUS_CODE,
    USER_EXIST_STATUS_CODE,
)
from database.connection import get_session


class UserTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)

    def tearDown(self):
        clean_database(self.session)

    def test_register_feature(self):
        response = test_client.post(
                    REGISTER_FULL_ROUTE,
                    json={USERNAME_KEY: FIRST_TEST_USER_USERNAME, PASSWORD_KEY: FIRST_TEST_USER_PASSWORD}
                ) 

        assert response.status_code == HTTP_200_OK
        data = response.json()
        assert data[USERID_KEY] == 1
        assert data[USERNAME_KEY] == FIRST_TEST_USER_USERNAME 

        _, users = self.user_controller.get_all_users()
        assert len(users) == 1

        response = test_client.post(
                    REGISTER_FULL_ROUTE,
                    json={USERNAME_KEY: FIRST_TEST_USER_USERNAME, PASSWORD_KEY: FIRST_TEST_USER_PASSWORD}
                )

        assert response.status_code == USER_EXIST_STATUS_CODE

    def test_loggin_feature(self):
        createAnUserBy(self.user_controller)

        response = test_client.post(
                    LOGIN_FULL_ROUTE,
                    data={USERNAME_KEY: FIRST_TEST_USER_USERNAME, PASSWORD_KEY: FIRST_TEST_USER_PASSWORD}
                )

        assert response.status_code == HTTP_200_OK
        assert response.json()[USER_KEY][USERNAME_KEY] == FIRST_TEST_USER_USERNAME
        assert response.json()[TOKEN_KEY] is not None

        response = test_client.post(
                    LOGIN_FULL_ROUTE,
                    data={USERNAME_KEY: FIRST_TEST_USER_WRONG_USERNAME, PASSWORD_KEY: FIRST_TEST_USER_PASSWORD}
                )

        assert response.status_code == USER_DOES_NOT_EXIST_STATUS_CODE

        response = test_client.post(
                    LOGIN_FULL_ROUTE,
                    data={USERNAME_KEY: FIRST_TEST_USER_USERNAME, PASSWORD_KEY: FIRST_TEST_USER_NEW_PASSWORD}
                )

        assert response.status_code == USER_DOES_NOT_EXIST_STATUS_CODE
