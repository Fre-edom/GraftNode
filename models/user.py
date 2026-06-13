from pydantic import BaseModel
from datetime import datetime



class User(BaseModel):
    username: str
    id : str
    email: str