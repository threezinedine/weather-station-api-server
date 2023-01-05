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
        return self.session.query(User).filter(User.username == username).first()

    def create_new_user(self, username: str, password: str) -> None:
        user = User(username=username, password=password)

        self.session.add(user)
        self.session.commit()

    def get_all_users(self) -> List[User]:
        return []
