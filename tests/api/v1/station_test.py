import unittest
import pytest
from fastapi.testclient import TestClient

from main import app
from database.connection import get_session
from app.controllers import UserController
from tests import (
    USERNAME_KEY,
    PASSWORD_KEY,
)


class StationTest(unittest.TestCase):
    def setUp(self):
        self.test_client = TestClient(app)
        self.user_controller = UserController(next(get_db()))

    def tearDown(self):
        pass

    @unittest.skip("")
    def test_given_when_no_user_is_created_when_a_new_user_is_registered_then_returns_the_200_response_with_user_info(self):
        response = self.test_client.post(
                    REGISTER_ROUTE,
                    json={
                        USERNAME_KEY: "threezinedine",
                        PASSWORD_KEY: "threezinedine"
                    }
                )

        assert response.status_code == 200

        response_user_info = response.json()
        self.assertDictEqual(response_user_info, {
                "userId": 1,
                USERNAME_KEY: "threezinedine"
            })

    @unittest.skip("")
    def test_given_when_no_user_is_created_when_a_new_user_is_registered_then_that_user_should_be_created(self):
        self.test_client.post(
                    REGISTER_ROUTE,
                    json={
                        USERNAME_KEY: "threezinedine",
                        PASSWORD_KEY: "threezinedine"
                    }
                )

        user = self.user_controller.get_user_by_name(username="threezinedine")
        assert user.username == "threezinedine"
        assert user.userId == 1
