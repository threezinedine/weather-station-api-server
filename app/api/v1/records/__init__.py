from fastapi import APIRouter

from app import RECORD_ROUTE_BASE


router = APIRouter(prefix=RECORD_ROUTE_BASE, tags=["Records"])


from .records import *
