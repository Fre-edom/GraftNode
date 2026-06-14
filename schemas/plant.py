from pydantic import BaseModel, ConfigDict
from datetime import date


class PlantCreate(BaseModel):
    id_user: str
    id_planttype: str
    plant_petname: str | None = None
    plant_bio: str | None = None
    date_planted: date | None = None
    soil_type: str | None = None
    notes: str | None = None


class PlantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    plant_id: str
    id_user: str
    id_planttype: str
    plant_petname: str | None = None
    plant_bio: str | None = None
    date_planted: date | None = None
    soil_type: str | None = None
    notes: str | None = None