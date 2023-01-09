from app.constants import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
    HTTP_404_NOT_FOUND,
)


USER_DOES_NOT_EXIST_STATUS_CODE = HTTP_404_NOT_FOUND
USER_DOES_NOT_EXIST_DETAIL = "The user does not exist."

USER_DOES_NOT_EXIST_STATUS = {
    STATUS_CODE_KEY: USER_DOES_NOT_EXIST_STATUS_CODE,
    DETAIL_KEY: USER_DOES_NOT_EXIST_DETAIL
}
