import unittest
from fastapi.testclient import TestClient

from tests import (
    get_testing_session,
    clean_database,
)
from main import app
from app.controllers import UserController



class UserTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.test_client = TestClient(app)
        self.user_controller = UserController(self.session)

    def tearDown(self):
        clean_database(self.session)

    def test_when_no_user_is_created_when_register_new_user_then_success(self):
        response = self.test_client.post(
                    "/users/register",
                    json={"username": "threezinedine", "password": "threezinedine"}
                ) 

        assert response.status_code == 200
        
        data = response.json()
        assert data["userId"] == 1
        assert data["username"] == "threezinedine"

        _, users = self.user_controller.get_all_users()
        assert len(users) == 1
