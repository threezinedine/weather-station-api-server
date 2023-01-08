from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
)


NO_RELATIONSHIP_EXIST_STATUS_CODE = 404
NO_RELATIONSHIP_EXIST_DETAIL = "No relationship exists."

NO_RELATIONSHIP_EXIST_STATUS = {
    STATUS_CODE_KEY: NO_RELATIONSHIP_EXIST_STATUS_CODE,
    DETAIL_KEY: NO_RELATIONSHIP_EXIST_DETAIL
}

