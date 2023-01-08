from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
)


USER_DOES_NOT_EXIST_STATUS_CODE = 404
USER_DOES_NOT_EXIST_DETAIL = "The user does not exist."

USER_DOES_NOT_EXIST_STATUS = {
    STATUS_CODE_KEY: USER_DOES_NOT_EXIST_STATUS_CODE,
    DETAIL_KEY: USER_DOES_NOT_EXIST_DETAIL
}