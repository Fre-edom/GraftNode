from pydantic import BaseModel, ConfigDict
from datetime import date

class UserCreate(BaseModel):

    user_id: str
    email: str
    hashed_password: str
    date_created: date

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    email: str
    date_created: date