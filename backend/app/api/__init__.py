from fastapi import APIRouter

from .v1.routes import router as v1_router

api_router = APIRouter()
api_router.include_router(v1_router, prefix="")

__all__ = ["api_router"]
