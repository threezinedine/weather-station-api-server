from app.api.v1.users import router

from app.schemas import (
    RegisterOrLoginUserInfo,
    RegisterResponseUserInfo,
)


@router.post("/register", status_code=200)
def register_a_new_user(info: RegisterOrLoginUserInfo):
    response_user_info = RegisterResponseUserInfo(userId=1, username=info.username)
    return response_user_info
