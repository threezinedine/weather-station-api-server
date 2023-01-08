from sqlalchemy.orm import Session
from typing import (
    Union,
    List,
    Tuple,
    Dict,
)

from database.models import User
from app.exceptions import (
    OK_STATUS,
    USER_DOES_NOT_EXIST_STATUS,
    WRONG_PASSWORD_STATUS,
    USER_EXIST_STATUS,
    STATUS_CODE_KEY,
    DETAIL_KEY,
)


class UserController:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_name(self, username: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        status = OK_STATUS
        user = self.session.query(User).filter(User.username == username).first()

        if user is None:
            status = USER_DOES_NOT_EXIST_STATUS

        return status, user

    def get_user_by_id(self, userId:int) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        status = OK_STATUS
        user = self.session.query(User).filter(User.userId == userId).first()

        if user is None:
            status = USER_DOES_NOT_EXIST_STATUS

        return status, user

    def create_new_user(self, username: str, password: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        status = OK_STATUS
        _, user = self.get_user_by_name(username=username)
        new_user = None

        if user is not None:
            status = USER_EXIST_STATUS
        else:
            new_user = User(username, password)

            self.session.add(new_user)
            self.session.commit()

        return status, new_user

    def get_all_users(self) -> Tuple[Dict[str, Union[int, Union[str, None]]], List[User]]:
        return OK_STATUS, self.session.query(User).all()

    def get_user_by_username_and_password(self, username: str, password: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        status = OK_STATUS
        user = self.session.query(User).filter(User.username == username).first()

        if user is None:
            status = USER_DOES_NOT_EXIST_STATUS
        elif user is not None and not user.is_match(password):
            status = WRONG_PASSWORD_STATUS
            user = None

        return status, user 

    def _change_username(self, user: User, status: Dict[str, Union[int, Union[str, None]]], username: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        if username is not None:
            _, user_with_username = self.get_user_by_name(username)

            if user_with_username is None:
                user.username = username
                self.session.commit()
                result = True
            else:
                status = USER_EXIST_STATUS
                user = None

        return status, user

    def _change_password(self, user: User, status: Dict[str, Union[int, Union[str, None]]], password: str) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        if password is not None:
            user.set_new_password(password)
            self.session.commit()

        return status, user

    def change_user(self, username: str, new_username: str = None, new_password: str = None) -> Tuple[Dict[str, Union[int, Union[str, None]]], User]:
        status = OK_STATUS
        _, user = self.get_user_by_name(username=username)

        if user is None:
            status = USER_DOES_NOT_EXIST_STATUS
        else:
            status, user = self._change_username(user, status, new_username)
            status, user = self._change_password(user, status, new_password)

        return status, user

    def delete_all_users(self) -> Tuple[Dict[str, Union[int, Union[str, None]]], None]:
        status = OK_STATUS

        self.session.query(User).delete()
        self.session.commit()

        return status, None

    def delete_user_by_username(self, username: str) ->Tuple[Dict[str, Union[int, Union[str, None]]], None]:
        status = OK_STATUS

        _, user_with_username = self.get_user_by_name(username)

        if user_with_username is None:
            status = USER_DOES_NOT_EXIST_STATUS
        else:
            self.session.delete(user_with_username)
            self.session.commit()

        return status, None
