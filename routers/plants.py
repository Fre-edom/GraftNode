import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from models import User
from models.plant import Plant
from schemas.plant import PlantCreate, PlantUpdate, PlantRead

router = APIRouter(prefix="/plants", tags=["plants"])


# Every route here depends on get_current_user, which means:
#   - no valid token  -> FastAPI returns 401 BEFORE the function body runs
#   - a valid token   -> we hold the real User object, and take ownership
#                        (id_user) from IT, never from the request body.
# This is what closes the "broken access control" hole: a client can no
# longer create or read plants under someone else's account.


@router.post("/", response_model=PlantRead, status_code=201)
def create_plant(
    payload: PlantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plant = Plant(
        plant_id=str(uuid.uuid4()),
        id_user=current_user.user_id,        # owner = the logged-in user, from the token
        **payload.model_dump(),
    )
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant


@router.get("/", response_model=list[PlantRead])
def list_plants(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Only ever return the logged-in user's OWN plants.
    return db.query(Plant).filter(Plant.id_user == current_user.user_id).all()


@router.get("/{plant_id}", response_model=PlantRead)
def read_plant(
    plant_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plant = db.get(Plant, plant_id)
    # 404 (not 403) when it isn't yours — don't even reveal that it exists.
    if plant is None or plant.id_user != current_user.user_id:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant


@router.patch("/{plant_id}", response_model=PlantRead)
def update_plant(
    plant_id: str,
    payload: PlantUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plant = db.get(Plant, plant_id)
    if plant is None or plant.id_user != current_user.user_id:
        raise HTTPException(status_code=404, detail="Plant not found")
    # exclude_unset=True -> only overwrite the fields the client actually sent.
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(plant, field, value)
    db.commit()
    db.refresh(plant)
    return plant


@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant(
    plant_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plant = db.get(Plant, plant_id)
    if plant is None or plant.id_user != current_user.user_id:
        raise HTTPException(status_code=404, detail="Plant not found")
    db.delete(plant)
    db.commit()
    # 204 No Content = success with no response body.
