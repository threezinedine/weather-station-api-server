from fastapi import (
    Header,
    Depends,
    HTTPException,
)
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from typing import (
    Dict,
)
from datetime import datetime, timedelta

from app.constants import (
    USERNAME_KEY,
)


secret_key = os.getenv("SECRET_KEY", "secret_key")
auth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def generate_token(payload: Dict[str, str], expired_delta: timedelta = timedelta(minutes=15)) -> str:
    expire_time = datetime.utcnow() + expired_delta
    token = jwt.encode(dict(exp=expire_time, **payload), secret_key, algorithm="HS256")
    return token

def verify_token(token: str = Depends(auth2_scheme)) -> Dict[str, str]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
        print("Error: ", e)
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return payload[USERNAME_KEY]
