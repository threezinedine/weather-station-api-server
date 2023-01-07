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
    HTTP_200_OK,
)


class UserController:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_name(self, username: str) -> Tuple[Dict[str, Union[int, str]], User]:
        status = {}
        user = self.session.query(User).filter(User.username == username).first()

        if user is None:
            status[STATUS_CODE_KEY] = USERNAME_DOES_NOT_EXISTED_STATUS_CODE 
            status[DETAIL_KEY] = USERNAME_DOES_NOT_EXISTED_DETAIL
        else:
            status[STATUS_CODE_KEY] = HTTP_200_OK
            status[DETAIL_KEY] = None

        return status, user

    def get_user_by_id(self, userId:int) -> Union[User, None]:
        return self.session.query(User).filter(User.userId == userId).first()

    def create_new_user(self, username: str, password: str) -> Tuple[Dict[str, Union[int, str]], User]:
        status = {}
        user = User(username, password)

        status[STATUS_CODE_KEY] = 200 
        status[DETAIL_KEY] = None
        self.session.add(user)
        self.session.commit()

        return status, user

    def get_all_users(self) -> List[User]:
        return {STATUS_CODE_KEY: HTTP_200_OK, DETAIL_KEY: None}, self.session.query(User).all()
