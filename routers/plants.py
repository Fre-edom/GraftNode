import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.plant import Plant
from schemas.plant import PlantCreate, PlantRead

router = APIRouter(prefix="/plants", tags=["plants"])


@router.post("/", response_model=PlantRead, status_code=201)
def create_plant(payload: PlantCreate, db: Session = Depends(get_db)):
    plant = Plant(plant_id=str(uuid.uuid4()), **payload.model_dump())
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant


@router.get("/", response_model=list[PlantRead])
def list_plants(db: Session = Depends(get_db)):
    return db.query(Plant).all()


@router.get("/{plant_id}", response_model=PlantRead)
def read_plant(plant_id: str, db: Session = Depends(get_db)):
    plant = db.get(Plant, plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant
