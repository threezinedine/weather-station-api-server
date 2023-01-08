from app.exceptions import (
    DETAIL_KEY,
    STATUS_CODE_KEY,
)


NO_RECORD_EXIST_STATUS_CODE = 404
NO_RECORD_EXIST_DETAIL = "No record exists."


NO_RECORD_EXIST_STATUS = {
    STATUS_CODE_KEY: NO_RECORD_EXIST_STATUS_CODE,
    DETAIL_KEY: NO_RECORD_EXIST_DETAIL,
}
