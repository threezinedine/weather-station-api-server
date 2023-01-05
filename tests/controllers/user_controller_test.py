import unittest
import pytest 

from app.controllers import UserController
from database.connection import get_db
from database.models import User
from tests import get_testing_session


class UserControllerTest(unittest.TestCase):
    first_testing_username = "threezinedine"
    testing_password = "threezinedine1"
    second_first_testing_username = "threezinedineadasdf"
    second_testing_password = "daffasdgasd"
    wrong_first_testing_username = "threezinedine2"
    testing_new_user_password = "threezinedineadfab"

    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)

    def tearDown(self):
        self.session.query(User).delete()
        self.session.commit()
        self.session.close()

    def assertUser(self, user: User, username: str, password: str) -> None:
        assert user.username == username
        assert user.is_match(password)

    def test_given_no_user_is_created_when_controller_get_a_user_by_name_then_receives_None(self):
        user = self.user_controller.get_user_by_name(username=self.first_testing_username)
        assert user is None

    def test_given_no_user_is_created_when_create_a_new_user_then_that_user_is_created(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        user = self.user_controller.get_user_by_name(username=self.first_testing_username)

        self.assertUser(user, self.first_testing_username, self.testing_password)

    def test_given_a_user_is_created_when_asking_the_wrong_user_then_returns_False(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        user = self.user_controller.get_user_by_name(username=self.wrong_first_testing_username)

        assert user is None
        
    def test_given_no_user_is_created_when_asking_all_users_then_returns_an_empty_string(self):
        users = self.user_controller.get_all_users()

        self.assertListEqual(users, [])

    def test_given_a_user_is_created_when_asking_all_users_then_returns_the_list_contains_that_user(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        users = self.user_controller.get_all_users()

        assert len(users) == 1
        self.assertUser(users[0], self.first_testing_username, self.testing_password)

    def test_given_a_user_is_created_when_create_a_new_user_with_the_same_username_then_that_user_can_not_be_created_and_returns_False(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        result = self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_new_user_password)

        assert result == False
        users = self.user_controller.get_all_users()
        assert len(users) == 1

    def test_given_two_users_are_created_when_asking_by_id_that_is_existed_then_returns_correct_user(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)
        self.user_controller.create_new_user(username=self.second_first_testing_username, password=self.second_testing_password)

        first_user = self.user_controller.get_user_by_id(1)
        second_user = self.user_controller.get_user_by_id(2)

        self.assertUser(first_user, self.first_testing_username, self.testing_password)
        self.assertUser(second_user, self.second_first_testing_username, self.second_testing_password)

    def test_given_two_users_are_created_when_asking_by_non_existed_id_then_returns_None(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)
        self.user_controller.create_new_user(username=self.second_first_testing_username, password=self.second_testing_password)

        non_existed_user = self.user_controller.get_user_by_id(3)

        assert non_existed_user is None
