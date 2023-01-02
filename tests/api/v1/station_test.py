import unittest
import pytest
from fastapi.testclient import TestClient

from main import app
from database.connection import get_db
from app.controllers import UserController


class StationTest(unittest.TestCase):
    def setUp(self):
        self.test_client = TestClient(app)
        self.user_controller = UserController(next(get_db()))

    def tearDown(self):
        pass

    def test_given_when_no_user_is_created_when_a_new_user_is_registered_then_returns_the_200_response_with_user_info(self):
        response = self.test_client.post(
                    "/users/register",
                    json={
                        "username": "threezinedine",
                        "password": "threezinedine"
                    }
                )

        assert response.status_code == 200

        response_user_info = response.json()
        self.assertDictEqual(response_user_info, {
                "userId": 1,
                "username": "threezinedine"
            })

    def test_given_when_no_user_is_created_when_a_new_user_is_registered_then_that_user_should_be_created(self):
        self.test_client.post(
                    "/users/register",
                    json={
                        "username": "threezinedine",
                        "password": "threezinedine"
                    }
                )
