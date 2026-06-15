from typing import Annotated
from fastapi import  Depends
from sqlmodel import Session    
from database import get_db
from models.user import User
from security import oauth2_scheme, decode_access_token



def get_current_user(
         token: Annotated[str, Depends(oauth2_scheme)],
         db : Session = Depends(get_db)
         
) -> User:pass