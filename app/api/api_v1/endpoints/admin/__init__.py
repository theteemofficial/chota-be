from fastapi import APIRouter

from . import auth, recommendation, category


# Global admin routes.
router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["admin/authentication"])
router.include_router(
    recommendation.router, prefix="/recommendation", tags=["admin/recommendation"]
)
router.include_router(category.router, prefix="/category", tags=["admin/category"])
