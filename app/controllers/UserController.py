from sqlalchemy.orm import Session
from typing import (
    Union,
    List,
)

from database.models import User


class UserController:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_name(self, username: str) -> Union[User, None]:
        status = {}
        user = self.session.query(User).filter(User.username == username).first()

        status["status_code"] = 404 
        status["detail"] = "The userId does not exist."

        return status, user

    def get_user_by_id(self, userId:int) -> Union[User, None]:
        return self.session.query(User).filter(User.userId == userId).first()

    def create_new_user(self, username: str, password: str) -> bool:
        result = False
        user = self.get_user_by_name(username=username)

        if user is None:
            new_user = User(username=username, password=password)
            self.session.add(new_user)
            self.session.commit()
            result = True

        return result

    def get_all_users(self) -> List[User]:
        return self.session.query(User).all()
