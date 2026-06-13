from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PlantCreate(BaseModel):
    name: str
    description: str | None = None
    category: str


class PlantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    description: str | None = None
    category: str
    date_created: datetime

    


