from fastapi import FastAPI
from database import engine, Base
from routers import router
from models import User, PlantCategory, PlantType, Plant

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plant_OS", description="A Plant Management System", version="1.0.0")
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "healthy"}
    