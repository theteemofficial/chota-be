from fastapi import APIRouter

from . import auth, recommendation


# Global admin routes.
router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["admin/authentication"])
router.include_router(
    recommendation.router, prefix="/recommendation", tags=["admin/recommendation"]
)
