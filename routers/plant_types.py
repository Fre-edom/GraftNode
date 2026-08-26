from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from models import User
from models.plant_type import PlantType
from schemas.plant_type import PlantTypeCreate, PlantTypeRead

# Plant types are SHARED reference data (a taxonomy), not per-user.
# Every route still requires a logged-in user for consistency.
router = APIRouter(prefix="/plant-types", tags=["plant-types"])


@router.post("/", response_model=PlantTypeRead, status_code=201)
def create_plant_type(
    payload: PlantTypeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plant_type = PlantType(**payload.model_dump())
    db.add(plant_type)
    db.commit()
    db.refresh(plant_type)
    return plant_type


@router.get("/", response_model=list[PlantTypeRead])
def list_plant_types(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(PlantType).all()


@router.get("/{type_id}", response_model=PlantTypeRead)
def read_plant_type(
    type_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plant_type = db.get(PlantType, type_id)
    if plant_type is None:
        raise HTTPException(status_code=404, detail="Plant type not found")
    return plant_type
