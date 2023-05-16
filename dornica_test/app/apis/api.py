from fastapi import APIRouter
from app.apis.endpoints import root, auth
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(root.router, tags=["root"])
api_router.include_router(auth.router, prefix=settings.AUTH_ROUTE_PREFIX, tags=["auth"])
