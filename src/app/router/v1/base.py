from fastapi import APIRouter
from .user import router as user

router = APIRouter()

router.include_router(user, prefix="/api/v1")
