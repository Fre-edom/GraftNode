from pydantic import BaseModel, ConfigDict
from datetime import date

class UserCreate(BaseModel):
    user_id: str
    email: str
    password: str
    date_created: date
    user_type: str | None = None

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    email: str
    date_created: date
    user_type: str | None = None



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"