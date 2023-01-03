from sqlalchemy.orm import Session

from database.models import User


class UserController:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_name(self, username: str) -> User:
        return None
