from fastapi import APIRouter


router = APIRouter(prefix="/users")


from .users import *
