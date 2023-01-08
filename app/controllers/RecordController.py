from sqlalchemy.orm import Session


class RecordController:
    def __init__(self, session: Session):
        self.session = session
