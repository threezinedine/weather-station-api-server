import unittest
import pytest
from fastapi.testclient import TestClient

from main import app
from database.connection import get_db


class StationTest(unittest.TestCase):
    def setUp(self):
        self.test_client = TestClient(app)

    def tearDown(self):
        pass

    def test_given_when_no_user_is_created_when_a_new_user_is_registered_then_that_user_should_be_created(self):
        response = self.test_client.post(
                    "/users/register",
                    json={
                        "username": "threezinedine",
                        "password": "threezinedine"
                    }
                )

        assert response.status_code == 200
