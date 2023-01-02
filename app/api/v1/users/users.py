from app.api.v1.users import router

from app.schemas import (
    RegisterOrLoginUserInfo,
)


@router.post("/register", status_code=200)
def register_a_new_user(info: RegisterOrLoginUserInfo):
    return {}
