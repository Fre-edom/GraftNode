from fastapi import APIRouter
from routers.plants import router as plants_router
from routers.plant_categories import router as categories_router
from routers.plant_types import router as types_router
from routers.auth import router as auth_router

router = APIRouter()
router.include_router(plants_router)
router.include_router(categories_router)
router.include_router(types_router)
router.include_router(auth_router)

__all__ = ["router"]