from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from database import setting


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # Bcrypt has a 72-byte limit, truncate if necessary
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Bcrypt has a 72-byte limit, truncate if necessary (same as hash_password)
    return pwd_context.verify(plain_password[:72], hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=setting.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, setting.secret_key, algorithm=setting.algorithm)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, setting.secret_key, algorithms=[setting.algorithm])
