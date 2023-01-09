from fastapi import APIRouter
from app import USER_BASE_ROUTE


router = APIRouter(prefix=USER_BASE_ROUTE, tags=["Users"])


from .users import *
