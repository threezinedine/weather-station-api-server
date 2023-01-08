STATUS_CODE_KEY = "status_code"
DETAIL_KEY = "detail"

HTTP_200_OK = 200

OK_STATUS = {
    STATUS_CODE_KEY: HTTP_200_OK,
    DETAIL_KEY: None
}

from .UserDoesNotExistException import *
from .UserExistException import *
from .WrongPasswordException import *
from .StationDoesNotExistException import *
from .StationExistException import *
from .NoRelationshipExistException import *
from .WrongStationKey import *
