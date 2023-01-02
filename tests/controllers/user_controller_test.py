import unittest
import pytest 

from app.controllers import UserController
from database.connection import get_db


class UserControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_db())
        self.user_controller = UserController(self.session)

    def tearDown(self):
        self.session.close()

    def test_given_no_user_is_created_when_controller_get_a_user_by_name_then_receives_None(self):
        user = self.user_controller.get_user_by_name(username="threezinedine")
        assert user is None
