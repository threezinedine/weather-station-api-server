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
)
from main import app
from app.controllers import UserController
from database.connection import get_session



class UserTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        app.dependency_overrides[get_session] = get_testing_session
        self.test_client = TestClient(app)
        self.user_controller = UserController(self.session)

    def tearDown(self):
        clean_database(self.session)

    def test_register_feature(self):
        response = self.test_client.post(
                    "/users/register",
                    json={"username": FIRST_TEST_USER_USERNAME, "password": FIRST_TEST_USER_PASSWORD}
                ) 

        assert response.status_code == 200
        
        data = response.json()
        assert data["userId"] == 1
        assert data["username"] == FIRST_TEST_USER_USERNAME 

        _, users = self.user_controller.get_all_users()
        assert len(users) == 1

        response = self.test_client.post(
                    "/users/register",
                    json={"username": FIRST_TEST_USER_USERNAME, "password": FIRST_TEST_USER_PASSWORD}
                )

        assert response.status_code == 409

    def test_loggin_feature(self):
        createAnUserBy(self.user_controller)

        response = self.test_client.post(
                    "/users/login",
                    json={"username": FIRST_TEST_USER_USERNAME, "password": FIRST_TEST_USER_PASSWORD}
                )

        assert response.status_code == 200
        assert response.json()["username"] == FIRST_TEST_USER_USERNAME

        response = self.test_client.post(
                    "/users/login",
                    json={"username": FIRST_TEST_USER_WRONG_USERNAME, "password": FIRST_TEST_USER_PASSWORD}
                )

        assert response.status_code == 404

        response = self.test_client.post(
                    "/users/login",
                    json={"username": FIRST_TEST_USER_USERNAME, "password": FIRST_TEST_USER_NEW_PASSWORD}
                )

        assert response.status_code == 404
