from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password:str) -> str:
    pass

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pass

def create_access_token(data: dict) -> str:
    pass

def decode_access_token(token: str) -> dict:
    pass
