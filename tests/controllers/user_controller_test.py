import unittest
import pytest 
from typing import (
    Dict,
    Union,
    List,
)

from app.controllers import UserController
from database.connection import get_db
from database.models import User
from tests import get_testing_session
from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
    OK_STATUS,
    USER_DOES_NOT_EXIST_STATUS,
    USER_EXIST_STATUS,
    WRONG_PASSWORD_STATUS,
)
from tests import (
    clean_database,
)
from tests.controllers import (
    assertStatus,
    assertUser,
    FIRST_TEST_USER_USERNAME,
    FIRST_TEST_USER_PASSWORD,
    SECOND_TEST_USER_USERNAME,
    SECOND_TEST_USER_PASSWORD,
    FIRST_TEST_USER_WRONG_USERNAME,
    NEW_TEST_USER_PASSWORD,
    FIRST_TEST_USER_NEW_USERNAME,
    FIRST_TEST_USER_NEW_PASSWORD,
    createAnUserBy,
    createTwoUsersBy,
)


class UserControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.user_controller = UserController(self.session)

    def tearDown(self):
        clean_database(self.session)

    def test_given_no_user_is_created_when_controller_get_a_user_by_name_then_receives_username_does_not_exist_and_None(self):
        status, user = self.user_controller.get_user_by_name(username=FIRST_TEST_USER_USERNAME)

        assertStatus(status, USER_DOES_NOT_EXIST_STATUS)
        assert user is None

    def test_given_no_user_is_created_when_create_a_new_user_then_return_ok_and_None(self):
        status, user = self.user_controller.create_new_user(username=FIRST_TEST_USER_USERNAME, password=FIRST_TEST_USER_PASSWORD)

        assertStatus(status, OK_STATUS)
        assertUser(user, FIRST_TEST_USER_USERNAME, FIRST_TEST_USER_PASSWORD)
        
    def test_given_a_user_is_created_when_querying_user_by_username_then_that_returns_ok_and_that_user(self):
        createAnUserBy(self.user_controller)

        status, user = self.user_controller.get_user_by_name(username=FIRST_TEST_USER_USERNAME)

        assertStatus(status, OK_STATUS)
        assertUser(user, username=FIRST_TEST_USER_USERNAME, password=FIRST_TEST_USER_PASSWORD)

    def test_given_a_user_is_created_when_asking_the_wrong_user_then_returns_username_does_not_exist_and_none(self):
        createAnUserBy(self.user_controller)

        status, user = self.user_controller.get_user_by_name(username=FIRST_TEST_USER_WRONG_USERNAME)

        assertStatus(status, USER_DOES_NOT_EXIST_STATUS)
        assert user is None
        
    def test_given_no_user_is_created_when_asking_all_users_then_returns_an_empty_string(self):
        status, users = self.user_controller.get_all_users()

        assertStatus(status, OK_STATUS)
        self.assertListEqual(users, [])

    def test_given_a_user_is_created_when_asking_all_users_then_returns_the_list_contains_that_user(self):
        createAnUserBy(self.user_controller)

        status, users = self.user_controller.get_all_users()

        assertStatus(status, OK_STATUS)
        assert len(users) == 1
        assertUser(users[0], FIRST_TEST_USER_USERNAME, FIRST_TEST_USER_PASSWORD)

    def test_given_a_user_is_created_when_create_a_new_user_with_the_same_username_then_returns_username_existed_and_None(self):
        createAnUserBy(self.user_controller)

        status, user = self.user_controller.create_new_user(username=FIRST_TEST_USER_USERNAME, password=NEW_TEST_USER_PASSWORD)

        assertStatus(status, USER_EXIST_STATUS)
        assert user is None
        _, users = self.user_controller.get_all_users()
        assert len(users) == 1

    def test_given_two_users_are_created_when_asking_by_id_that_is_existed_then_returns_ok_and_user(self):
        createTwoUsersBy(self.user_controller)

        first_status, first_user = self.user_controller.get_user_by_id(1)
        second_status, second_user = self.user_controller.get_user_by_id(2)

        assertStatus(first_status, OK_STATUS)
        assertStatus(second_status, OK_STATUS)

        assertUser(first_user, FIRST_TEST_USER_USERNAME, FIRST_TEST_USER_PASSWORD)
        assertUser(second_user, SECOND_TEST_USER_USERNAME, SECOND_TEST_USER_PASSWORD)

    def test_given_two_users_are_created_when_asking_by_non_existed_id_then_returns_username_is_not_existed_and_none(self):
        createTwoUsersBy(self.user_controller)

        status, user = self.user_controller.get_user_by_id(3)

        assertStatus(status, USER_DOES_NOT_EXIST_STATUS)
        assert user is None

    def test_given_a_user_is_created_when_querying_user_by_valid_username_and_password_then_return_ok_and_user(self):
        createAnUserBy(self.user_controller)

        status, user = self.user_controller.get_user_by_username_and_password(FIRST_TEST_USER_USERNAME, FIRST_TEST_USER_PASSWORD)

        assertStatus(status, OK_STATUS)
        assertUser(user, FIRST_TEST_USER_USERNAME, FIRST_TEST_USER_PASSWORD)

    def test_given_no_user_created_when_querying_user_by_invalid_username_then_return_user_does_not_exist_and_none(self):
        createAnUserBy(self.user_controller)

        status, user = self.user_controller.get_user_by_username_and_password(FIRST_TEST_USER_WRONG_USERNAME, FIRST_TEST_USER_PASSWORD)

        assertStatus(status, USER_DOES_NOT_EXIST_STATUS)
        assert user is None

    def test_given_a_user_is_created_when_querying_user_by_valid_username_and_invalid_password_then_returns_password_is_wrong_and_none(self):
        createAnUserBy(self.user_controller)

        status, user = self.user_controller.get_user_by_username_and_password(FIRST_TEST_USER_USERNAME, FIRST_TEST_USER_WRONG_USERNAME)

        assertStatus(status, WRONG_PASSWORD_STATUS)
        assert user is None

    def test_given_no_user_is_created_when_change_the_name_of_non_existed_username_then_returns_user_does_not_existed_exception_and_none(self):
        createAnUserBy(self.user_controller)

        status, user = self.user_controller.change_user(username=FIRST_TEST_USER_WRONG_USERNAME, new_username=FIRST_TEST_USER_NEW_USERNAME)

        assertStatus(status, USER_DOES_NOT_EXIST_STATUS)
        assert user is None

    def test_given_a_user_is_created_when_change_the_name_of_existed_username_then_returns_ok_and_that_user(self):
        createAnUserBy(self.user_controller)

        status, user = self.user_controller.change_user(username=FIRST_TEST_USER_USERNAME, new_username=FIRST_TEST_USER_NEW_USERNAME)
        
        assertStatus(status, OK_STATUS)
        assertUser(user, FIRST_TEST_USER_NEW_USERNAME, FIRST_TEST_USER_PASSWORD)
        _, modified_user = self.user_controller.get_user_by_name(FIRST_TEST_USER_NEW_USERNAME)
        assertUser(modified_user, FIRST_TEST_USER_NEW_USERNAME, FIRST_TEST_USER_PASSWORD)

    def test_given_two_users_are_created_when_change_the_name_of_the_first_user_with_the_name_of_the_second_user_then_returns_username_existed_and_None(self):
        createTwoUsersBy(self.user_controller)

        status, user = self.user_controller.change_user(username=FIRST_TEST_USER_USERNAME, new_username=SECOND_TEST_USER_USERNAME)

        assertStatus(status, USER_EXIST_STATUS)
        assert user is None

    def test_given_a_user_is_created_when_change_the_password_then_returns_ok_and_that_user(self):
        createAnUserBy(self.user_controller)

        status, user = self.user_controller.change_user(username=FIRST_TEST_USER_USERNAME, new_password=FIRST_TEST_USER_NEW_PASSWORD)

        assertStatus(status, OK_STATUS)
        assertUser(user, FIRST_TEST_USER_USERNAME, FIRST_TEST_USER_NEW_PASSWORD)
        _, modified_user = self.user_controller.get_user_by_name(FIRST_TEST_USER_USERNAME)
        assertUser(modified_user, FIRST_TEST_USER_USERNAME, FIRST_TEST_USER_NEW_PASSWORD)

    def test_given_a_user_is_created_when_change_both_valid_username_and_password_then_returns_ok_and_that_user(self):
        createAnUserBy(self.user_controller)

        status, user = self.user_controller.change_user(username=FIRST_TEST_USER_USERNAME, 
                        new_username=FIRST_TEST_USER_NEW_USERNAME, new_password=FIRST_TEST_USER_NEW_PASSWORD)

        assertStatus(status, OK_STATUS)
        assertUser(user, FIRST_TEST_USER_NEW_USERNAME, FIRST_TEST_USER_NEW_PASSWORD)
        _, modified_user = self.user_controller.get_user_by_name(FIRST_TEST_USER_NEW_USERNAME)
        assertUser(modified_user, FIRST_TEST_USER_NEW_USERNAME, FIRST_TEST_USER_NEW_PASSWORD)

    def test_given_two_users_are_created_when_delete_all_users_then_returns_ok_and_None(self):
        createTwoUsersBy(self.user_controller)

        status, user = self.user_controller.delete_all_users()

        assertStatus(status, OK_STATUS)
        assert user is None

        _, users = self.user_controller.get_all_users()
        self.assertListEqual(users, [])

    def test_given_two_users_are_created_when_deleting_that_user_by_valid_username_then_returns_ok_and_none(self):
        createTwoUsersBy(self.user_controller)

        status, user = self.user_controller.delete_user_by_username(FIRST_TEST_USER_USERNAME)

        assertStatus(status, OK_STATUS)
        assert user is None

        _, remain_users = self.user_controller.get_all_users()
        assert len(remain_users) == 1
        assertUser(remain_users[0], SECOND_TEST_USER_USERNAME, SECOND_TEST_USER_PASSWORD)

    def test_given_two_user_are_created_when_deleting_user_by_invalid_username_then_returns_username_does_not_existed_exception_and_none(self):
        createTwoUsersBy(self.user_controller)

        status, user = self.user_controller.delete_user_by_username(FIRST_TEST_USER_WRONG_USERNAME)

        assertStatus(status, USER_DOES_NOT_EXIST_STATUS)
        assert user is None

        _, remain_users = self.user_controller.get_all_users()
        assert len(remain_users) == 2
        assertUser(remain_users[0], FIRST_TEST_USER_USERNAME, FIRST_TEST_USER_PASSWORD)
        assertUser(remain_users[1], SECOND_TEST_USER_USERNAME, SECOND_TEST_USER_PASSWORD)
