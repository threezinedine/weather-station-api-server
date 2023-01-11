from fastapi import (
    Depends,
    HTTPException,
    Request,
    Form,
)
from sqlalchemy.orm import Session
from typing import (
    Dict
)

from app.api.v1.users import router
from app.schemas import (
    RegisterOrLoginUserInfo,
    RegisterResponseUserInfo,
    LoginResponseUserInfo,
)
from app.auth import (
    generate_token,
    verify_token,
)
from app.constants import (
    USERNAME_KEY,
    PASSWORD_KEY,
)
from app.controllers import UserController
from database.connection import get_session
from app.exceptions import (
    STATUS_CODE_KEY,
    DETAIL_KEY,
    HTTP_200_OK,
)
from app import (
    LOGIN_ROUTE,
    REGISTER_ROUTE,
    TOKEN_VALIDATION_ROUTE,
)
from app.constants import (
    USERNAME_KEY,
    PASSWORD_KEY,
)


@router.post(REGISTER_ROUTE, 
        status_code=HTTP_200_OK,
        response_model=RegisterResponseUserInfo)
def register_a_new_user(info: RegisterOrLoginUserInfo, session: Session = Depends(get_session)):
    user_controller = UserController(session)
    status, user = user_controller.create_new_user(username=info.username, password=info.password)

    if status[STATUS_CODE_KEY] != HTTP_200_OK:
        raise HTTPException(status_code=status[STATUS_CODE_KEY], detail=status[DETAIL_KEY])

    return user

@router.post(LOGIN_ROUTE,
        status_code=HTTP_200_OK,
        response_model=LoginResponseUserInfo)
def login_a_new_user(username: str = Form(), password: str = Form(), session: Session = Depends(get_session)):
    user_controller = UserController(session)
    status, user = user_controller.get_user_by_username_and_password(username, password)

    if status[STATUS_CODE_KEY] != HTTP_200_OK:
        raise HTTPException(status_code=status[STATUS_CODE_KEY], detail=status[DETAIL_KEY])

    response = LoginResponseUserInfo(user = user, token=generate_token({
            USERNAME_KEY: user.username
        }))

    return response

@router.get(TOKEN_VALIDATION_ROUTE,
        status_code=HTTP_200_OK)
def validate_validation(username: str = Depends(verify_token)):
    return {}

