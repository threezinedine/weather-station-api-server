import unittest
import pytest 
from typing import (
    Dict,
    Union,
)

from app.controllers import UserController
from database.connection import get_db
from database.models import User
from tests import get_testing_session
from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
    USERNAME_DOES_NOT_EXISTED_DETAIL,
    USERNAME_DOES_NOT_EXISTED_STATUS_CODE,
    USERNAME_EXISTED_DETAIL,
    USERNAME_EXISTED_STATUS_CODE,
    USERID_DOES_NOT_EXISTED_DETAIL,
    USERID_DOES_NOT_EXISTED_STATUS_CODE,
    WRONG_PASSWORD_DETAIL,
    WRONG_PASSWORD_STATUS_CODE,
    HTTP_200_OK,
)


class UserControllerTest(unittest.TestCase):
    first_testing_username = "threezinedine"
    testing_password = "threezinedine1"
    second_first_testing_username = "threezinedineadasdf"
    second_testing_password = "daffasdgasd"
    wrong_first_testing_username = "threezinedine2"
    testing_new_user_password = "threezinedineadfab"
    testing_changed_username = "testing_changed_username"
    testing_changed_password = "testing_changed_password"

    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)

    def tearDown(self):
        self.session.query(User).delete()
        self.session.commit()
        self.session.close()

    def assertStatus(self, status: Dict[str, Union[int, Union[str, None]]], status_code: int, status_detail: Union[str, None] = None):
        assert status[STATUS_CODE_KEY] == status_code
        assert status[DETAIL_KEY] == status_detail

    def assertUser(self, user: User, username: str, password: str) -> None:
        assert user.username == username
        assert user.is_match(password)

    def test_given_no_user_is_created_when_controller_get_a_user_by_name_then_receives_username_does_not_exist_and_None(self):
        status, user = self.user_controller.get_user_by_name(username=self.first_testing_username)

        self.assertStatus(status, USERNAME_DOES_NOT_EXISTED_STATUS_CODE, USERNAME_DOES_NOT_EXISTED_DETAIL)
        assert user is None

    def test_given_no_user_is_created_when_create_a_new_user_then_return_ok_and_None(self):
        status, user = self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        self.assertStatus(status, HTTP_200_OK)
        self.assertUser(user, self.first_testing_username, self.testing_password)
        
    def test_given_a_user_is_created_when_querying_user_by_username_then_that_returns_ok_and_that_user(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        status, user = self.user_controller.get_user_by_name(username=self.first_testing_username)

        self.assertStatus(status, HTTP_200_OK)
        self.assertUser(user, username=self.first_testing_username, password=self.testing_password)

    def test_given_a_user_is_created_when_asking_the_wrong_user_then_returns_username_does_not_exist_and_none(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        status, user = self.user_controller.get_user_by_name(username=self.wrong_first_testing_username)

        self.assertStatus(status, USERNAME_DOES_NOT_EXISTED_STATUS_CODE, USERNAME_DOES_NOT_EXISTED_DETAIL)
        assert user is None
        
    def test_given_no_user_is_created_when_asking_all_users_then_returns_an_empty_string(self):
        status, users = self.user_controller.get_all_users()

        self.assertStatus(status, HTTP_200_OK)
        self.assertListEqual(users, [])

    def test_given_a_user_is_created_when_asking_all_users_then_returns_the_list_contains_that_user(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        status, users = self.user_controller.get_all_users()

        self.assertStatus(status, HTTP_200_OK)
        assert len(users) == 1
        self.assertUser(users[0], self.first_testing_username, self.testing_password)

    def test_given_a_user_is_created_when_create_a_new_user_with_the_same_username_then_returns_username_existed_and_None(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        status, user = self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_new_user_password)

        self.assertStatus(status, USERNAME_EXISTED_STATUS_CODE, USERNAME_EXISTED_DETAIL)
        assert user is None
        _, users = self.user_controller.get_all_users()
        assert len(users) == 1

    def test_given_two_users_are_created_when_asking_by_id_that_is_existed_then_returns_ok_and_user(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)
        self.user_controller.create_new_user(username=self.second_first_testing_username, password=self.second_testing_password)

        first_status, first_user = self.user_controller.get_user_by_id(1)
        second_status, second_user = self.user_controller.get_user_by_id(2)

        self.assertStatus(first_status, HTTP_200_OK)
        self.assertStatus(second_status, HTTP_200_OK)

        self.assertUser(first_user, self.first_testing_username, self.testing_password)
        self.assertUser(second_user, self.second_first_testing_username, self.second_testing_password)

    def test_given_two_users_are_created_when_asking_by_non_existed_id_then_returns_username_is_not_existed_and_none(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)
        self.user_controller.create_new_user(username=self.second_first_testing_username, password=self.second_testing_password)

        status, user = self.user_controller.get_user_by_id(3)

        self.assertStatus(status, USERID_DOES_NOT_EXISTED_STATUS_CODE, USERID_DOES_NOT_EXISTED_DETAIL)
        assert user is None

    def test_given_a_user_is_created_when_querying_user_by_valid_username_and_password_then_return_ok_and_user(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        status, user = self.user_controller.get_user_by_username_and_password(self.first_testing_username, self.testing_password)

        self.assertStatus(status, HTTP_200_OK)
        self.assertUser(user, self.first_testing_username, self.testing_password)

    def test_given_no_user_created_when_querying_user_by_invalid_username_then_return_user_does_not_exist_and_none(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        status, user = self.user_controller.get_user_by_username_and_password(self.wrong_first_testing_username, self.testing_password)

        self.assertStatus(status, USERNAME_DOES_NOT_EXISTED_STATUS_CODE, USERNAME_DOES_NOT_EXISTED_DETAIL)
        assert user is None

    def test_given_a_user_is_created_when_querying_user_by_valid_username_and_invalid_password_then_returns_password_is_wrong_and_none(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        status, user = self.user_controller.get_user_by_username_and_password(self.first_testing_username, self.wrong_first_testing_username)

        self.assertStatus(status, WRONG_PASSWORD_STATUS_CODE, WRONG_PASSWORD_DETAIL)
        assert user is None

    def test_given_no_user_is_created_when_change_the_name_of_non_existed_username_then_returns_user_does_not_existed_exception_and_none(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_new_user_password)

        status, user = self.user_controller.change_user(username=self.wrong_first_testing_username, new_username=self.testing_changed_username)

        self.assertStatus(status, USERNAME_DOES_NOT_EXISTED_STATUS_CODE, USERNAME_DOES_NOT_EXISTED_DETAIL)
        assert user is None

    def test_given_a_user_is_created_when_change_the_name_of_existed_username_then_returns_ok_and_that_user(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_new_user_password)

        status, user = self.user_controller.change_user(username=self.first_testing_username, new_username=self.testing_changed_username)
        
        self.assertStatus(status, HTTP_200_OK)
        self.assertUser(user, self.testing_changed_username, self.testing_new_user_password)
        _, modified_user = self.user_controller.get_user_by_name(self.testing_changed_username)
        self.assertUser(modified_user, self.testing_changed_username, self.testing_new_user_password)

    def test_given_two_users_are_created_when_change_the_name_of_the_first_user_with_the_name_of_the_second_user_then_returns_username_existed_and_None(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)
        self.user_controller.create_new_user(username=self.second_first_testing_username, password=self.second_testing_password)

        status, user = self.user_controller.change_user(username=self.first_testing_username, new_username=self.second_first_testing_username)

        self.assertStatus(status, USERNAME_EXISTED_STATUS_CODE, USERNAME_EXISTED_DETAIL)
        assert user is None

    def test_given_a_user_is_created_when_change_the_password_then_returns_ok_and_that_user(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        status, user = self.user_controller.change_user(username=self.first_testing_username, new_password=self.testing_changed_password)

        self.assertStatus(status, HTTP_200_OK)
        self.assertUser(user, self.first_testing_username, self.testing_changed_password)
        _, modified_user = self.user_controller.get_user_by_name(self.first_testing_username)
        self.assertUser(modified_user, self.first_testing_username, self.testing_changed_password)

    def test_given_a_user_is_created_when_change_both_valid_username_and_password_then_returns_ok_and_that_user(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        status, user = self.user_controller.change_user(username=self.first_testing_username, 
                        new_username=self.testing_changed_username, new_password=self.testing_changed_password)

        self.assertStatus(status, HTTP_200_OK)
        self.assertUser(user, self.testing_changed_username, self.testing_changed_password)
        _, modified_user = self.user_controller.get_user_by_name(self.testing_changed_username)
        self.assertUser(modified_user, self.testing_changed_username, self.testing_changed_password)

    def test_given_two_users_are_created_when_delete_all_users_then_returns_ok_and_None(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)
        self.user_controller.create_new_user(username=self.second_first_testing_username, password=self.second_testing_password)

        status, user = self.user_controller.delete_all_users()

        self.assertStatus(status, HTTP_200_OK)
        assert user is None

        _, users = self.user_controller.get_all_users()
        self.assertListEqual(users, [])

    def test_given_a_user_is_created_when_deleting_that_user_by_valid_username_then_returns_ok_and_none(self):
        self.user_controller.create_new_user(username=self.first_testing_username, password=self.testing_password)

        status, user = self.user_controller.delete_user_by_username(self.first_testing_username)

        self.assertStatus(status, HTTP_200_OK)
        assert user is None
