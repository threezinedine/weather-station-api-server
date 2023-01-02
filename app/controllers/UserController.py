from sqlalchemy.orm import Session


class UserController:
    def __init__(self, session: Session):
        self.session = session
