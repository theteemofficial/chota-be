from fastapi import APIRouter


# import your endpoints here
from app.api.api_v1.endpoints import (
    admin,
    # business,
)

api_router = APIRouter()


# routes
# api_router.include_router(business.router, prefix="/business")

# Admin routes
api_router.include_router(
    admin.router,
    prefix="/admin",
)
