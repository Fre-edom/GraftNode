import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.item_model import ItemModel
from models.item import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    item = ItemModel(id=str(uuid.uuid4()), **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/", response_model=list[ItemRead])
def list_items(db: Session = Depends(get_db)):
    return db.query(ItemModel).all()


@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: str, db: Session = Depends(get_db)):
    item = db.get(ItemModel, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
