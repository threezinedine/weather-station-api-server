from fastapi import (
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.api.v1.users import router
from app.schemas import (
    RegisterOrLoginUserInfo,
    RegisterResponseUserInfo,
)
from app.controllers import UserController
from database.connection import get_session
from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
    HTTP_200_OK,
)


@router.post("/register", 
        status_code=HTTP_200_OK,
        response_model=RegisterResponseUserInfo)
def register_a_new_user(info: RegisterOrLoginUserInfo, session: Session = Depends(get_session)):
    user_controller = UserController(session)
    status, user = user_controller.create_new_user(username=info.username, password=info.password)

    if status[STATUS_CODE_KEY] != HTTP_200_OK:
        raise HTTPException(status_code=status[STATUS_CODE_KEY], detail=status[DETAIL_KEY])

    return user

@router.post("/login",
        status_code=HTTP_200_OK,
        response_model=RegisterResponseUserInfo)
def login_a_new_user(info: RegisterOrLoginUserInfo, session: Session = Depends(get_session)):
    user_controller = UserController(session)
    status, user = user_controller.get_user_by_username_and_password(info.username, info.password)

    if status[STATUS_CODE_KEY] != HTTP_200_OK:
        raise HTTPException(status_code=status[STATUS_CODE_KEY], detail=status[DETAIL_KEY])

    return user
