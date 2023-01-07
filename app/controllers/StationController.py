from sqlalchemy.orm import (
    Session,
)


class StationController:
    def __init__(self, session: Session):
        self.session = session
