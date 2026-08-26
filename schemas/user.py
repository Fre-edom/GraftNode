from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str
    user_type: str | None = None

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    email: str
    date_created: datetime
    user_type: str | None = None



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"