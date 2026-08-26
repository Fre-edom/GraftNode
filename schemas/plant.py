from pydantic import BaseModel, ConfigDict
from datetime import date


# Fields the CLIENT sends when creating a plant.
# NOTE: id_user is intentionally NOT here. The owner is taken from the
# logged-in user's token inside the router — never trusted from the request
# body. (Before, the client could set id_user to anyone: a security hole.)
class PlantCreate(BaseModel):
    id_planttype: str
    plant_petname: str | None = None
    plant_bio: str | None = None
    date_planted: date | None = None
    soil_type: str | None = None
    notes: str | None = None


# Fields the client MAY send when updating a plant. All optional:
# send only the fields you want to change (PATCH-style, partial update).
class PlantUpdate(BaseModel):
    id_planttype: str | None = None
    plant_petname: str | None = None
    plant_bio: str | None = None
    date_planted: date | None = None
    soil_type: str | None = None
    notes: str | None = None


# What we send BACK to the client. from_attributes lets Pydantic read
# straight off the SQLAlchemy object.
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
