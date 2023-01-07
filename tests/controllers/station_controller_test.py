import unittest

from database.models import (
    User,
    Station,
)
from app.controllers import (
    StationController,
)
from tests import (
    get_testing_session,
)


class StationControllerTest(unittest.TestCase):
    def setUp(self):
        self.session = next(get_testing_session())
        self.station_controller = StationController(self.session)

    def tearDown(self):
        self.session.query(User).delete()
        self.session.query(Station).delete()
        self.session.commit()
        self.session.close()

    def test_given_no_user_is_created_when_querying_all_stations_then_returns_ok_and_empty_array(self):
        pass
