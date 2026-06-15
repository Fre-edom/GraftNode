from pydantic import BaseModel, ConfigDict


class PlantTypeCreate(BaseModel):
    type_name: str


class PlantTypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    type_id: str
    type_name: str