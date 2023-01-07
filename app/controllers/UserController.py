from sqlalchemy.orm import Session
from typing import (
    Union,
    List,
    Tuple,
    Dict,
)

from database.models import User
from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
    USERNAME_DOES_NOT_EXISTED_DETAIL,
    USERNAME_DOES_NOT_EXISTED_STATUS_CODE,
    USERNAME_EXISTED_DETAIL,
    USERNAME_EXISTED_STATUS_CODE,
    USERID_DOES_NOT_EXISTED_STATUS_CODE,
    USERID_DOES_NOT_EXISTED_DETAIL,
    HTTP_200_OK,
    WRONG_PASSWORD_DETAIL,
    WRONG_PASSWORD_STATUS_CODE,
)


class UserController:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_name(self, username: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        status = {}
        user = self.session.query(User).filter(User.username == username).first()

        if user is None:
            status[STATUS_CODE_KEY] = USERNAME_DOES_NOT_EXISTED_STATUS_CODE 
            status[DETAIL_KEY] = USERNAME_DOES_NOT_EXISTED_DETAIL
        else:
            status[STATUS_CODE_KEY] = HTTP_200_OK
            status[DETAIL_KEY] = None

        return status, user

    def get_user_by_id(self, userId:int) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        status_code = {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None} 
        user = self.session.query(User).filter(User.userId == userId).first()

        if user is None:
            status_code[STATUS_CODE_KEY] = USERID_DOES_NOT_EXISTED_STATUS_CODE
            status_code[DETAIL_KEY] = USERID_DOES_NOT_EXISTED_DETAIL

        return status_code, user

    def create_new_user(self, username: str, password: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        status = {}
        _, user = self.get_user_by_name(username=username)
        new_user = None

        if user is not None:
            status[STATUS_CODE_KEY] = USERNAME_EXISTED_STATUS_CODE
            status[DETAIL_KEY] = USERNAME_EXISTED_DETAIL
        else:
            new_user = User(username, password)

            status[STATUS_CODE_KEY] = HTTP_200_OK 
            status[DETAIL_KEY] = None

            self.session.add(new_user)
            self.session.commit()

        return status, new_user

    def get_all_users(self) -> Tuple[Dict[str, Union[int, Union[str, None]]], List[User]]:
        return {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}, self.session.query(User).all()

    def get_user_by_username_and_password(self, username: str, password: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        status = {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}
        user = self.session.query(User).filter(User.username == username).first()

        if user is None:
            status[STATUS_CODE_KEY] = USERNAME_DOES_NOT_EXISTED_STATUS_CODE
            status[DETAIL_KEY] = USERNAME_DOES_NOT_EXISTED_DETAIL
        elif user is not None and not user.is_match(password):
            status[STATUS_CODE_KEY] = WRONG_PASSWORD_STATUS_CODE
            status[DETAIL_KEY] = WRONG_PASSWORD_DETAIL
            user = None

        return status, user 

    def change_user(self, username: str, new_username: str = None, new_password: str = None) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        status = {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}
        _, user = self.get_user_by_name(username=username)

        if user is None:
            status[STATUS_CODE_KEY] = USERNAME_DOES_NOT_EXISTED_STATUS_CODE
            status[DETAIL_KEY] = USERNAME_DOES_NOT_EXISTED_DETAIL
        else:
            if new_username is not None:
                _, user_with_new_username = self.get_user_by_name(username=new_username)
                if user_with_new_username is None:
                    user.username = new_username
                    self.session.commit()
                else:
                    status[STATUS_CODE_KEY] = USERNAME_EXISTED_STATUS_CODE
                    status[DETAIL_KEY] = USERNAME_EXISTED_DETAIL
                    user = None
            elif new_password is not None:
                user.set_new_password(new_password)
                self.session.commit()

        return status, user
