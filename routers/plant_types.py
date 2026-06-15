import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.plant_type import PlantType
from schemas.plant_type import PlantTypeCreate, PlantTypeRead

router = APIRouter(prefix="/plant-types", tags=["plant-types"])


@router.post("/", response_model=PlantTypeRead, status_code=201)
def create_plant_type(payload: PlantTypeCreate, db: Session = Depends(get_db)):
    type = PlantType(**payload.model_dump())
    db.add(type)
    db.commit()
    db.refresh(type)
    return type


@router.get("/", response_model=list[PlantTypeRead])
def list_plant_types(db: Session = Depends(get_db)):
    return db.query(PlantType).all()


@router.get("/{plant_id}", response_model=PlantTypeRead)
def read_plant(plant_id: str, db: Session = Depends(get_db)):
    type = db.get(PlantType, plant_id)
    if type is None:
        raise HTTPException(status_code=404, detail="Plant type not found")
    return type
