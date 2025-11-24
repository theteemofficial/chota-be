from fastapi import APIRouter

from . import auth


# Global admin routes.
router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["admin/authentication"])
