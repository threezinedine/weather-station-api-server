from fastapi import APIRouter
from app import USER_BASE_ROUTE


router = APIRouter(prefix=USER_BASE_ROUTE)


from .users import *
