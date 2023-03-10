from app.constants import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
    HTTP_404_NOT_FOUND,
)


STATION_DOES_NOT_EXIST_STATUS_CODE = HTTP_404_NOT_FOUND
STATION_DOES_NOT_EXIST_DETAIL = "The station does not exist."

STATION_DOES_NOT_EXIST_STATUS = {
    STATUS_CODE_KEY: STATION_DOES_NOT_EXIST_STATUS_CODE,
    DETAIL_KEY: STATION_DOES_NOT_EXIST_DETAIL
}
