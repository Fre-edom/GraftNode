from fastapi import APIRouter
from routers.plants import router as plants_router
from routers.plant_categories import router as categories_router
from routers.plant_types import router as plant_types_router

router = APIRouter()
router.include_router(plants_router)
router.include_router(categories_router)
router.include_router(plant_types_router)

__all__ = ["router"]