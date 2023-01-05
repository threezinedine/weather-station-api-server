import unittest
import pytest 

from app.controllers import UserController
from database.connection import get_db
from database.models import User
from tests import get_testing_session


class UserControllerTest(unittest.TestCase):
    testing_username = "threezinedine"
    testing_password = "threezinedine1"

    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)

    def tearDown(self):
        self.session.query(User).delete()
        self.session.commit()
        self.session.close()

    def test_given_no_user_is_created_when_controller_get_a_user_by_name_then_receives_None(self):
        user = self.user_controller.get_user_by_name(username=self.testing_username)
        assert user is None

    def test_given_no_user_is_created_when_create_a_new_user_then_that_user_is_created(self):
        self.user_controller.create_new_user(username=self.testing_username, password=self.testing_password)

        user = self.user_controller.get_user_by_name(username=self.testing_username)

        assert user.username == self.testing_username
        assert user.is_match(self.testing_password)
