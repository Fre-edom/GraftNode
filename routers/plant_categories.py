from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import PlantCategory
from schemas.plant_category import PlantCategoryCreate, PlantCategoryRead

router = APIRouter(prefix="/plant-categories", tags=["plant-categories"])


@router.post("/", response_model=PlantCategoryRead, status_code=201)
def create_category(payload: PlantCategoryCreate, db: Session = Depends(get_db)):
    category = PlantCategory(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/", response_model=list[PlantCategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return db.query(PlantCategory).all()


@router.get("/{category_id}", response_model=PlantCategoryRead)
def read_category(category_id: str, db: Session = Depends(get_db)):
    category = db.get(PlantCategory, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category