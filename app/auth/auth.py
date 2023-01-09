import jwt
import os
from typing import (
    Dict,
)
from datetime import datetime, timedelta

secret_key = os.getenv("SECRET_KEY", "secret_key")


def generate_token(payload: Dict[str, str], expired_delta: timedelta = timedelta(minutes=15)) -> str:
    expire_time = datetime.utcnow() + expired_delta
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

def verify_token(token: str) -> Dict[str, str]:
    try:
        payload = jwt.decode(token, secret_key, algorithm=["HS256"])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return None
    
    return payload
