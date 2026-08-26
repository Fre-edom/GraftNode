from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from models import User, PlantCategory
from schemas.plant_category import PlantCategoryCreate, PlantCategoryRead

# Plant categories are SHARED reference data (a taxonomy), not per-user.
# Every route still requires a logged-in user (get_current_user) so the API
# is consistent: nothing is reachable without a valid token.
router = APIRouter(prefix="/plant-categories", tags=["plant-categories"])


@router.post("/", response_model=PlantCategoryRead, status_code=201)
def create_category(
    payload: PlantCategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = PlantCategory(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/", response_model=list[PlantCategoryRead])
def list_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(PlantCategory).all()


@router.get("/{category_id}", response_model=PlantCategoryRead)
def read_category(
    category_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = db.get(PlantCategory, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
