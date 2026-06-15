from pydantic import BaseModel, ConfigDict


class PlantCategoryCreate(BaseModel):
    category_name: str


class PlantCategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    category_id: str
    category_name: str