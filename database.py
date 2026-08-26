from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    # extra="ignore" -> tolerate unrelated keys in .env instead of crashing
    # (same pattern as library_backend).
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

        
setting = Settings()
engine = create_engine(setting.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()