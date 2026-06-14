from fastapi import FastAPI
from database import engine, Base
from routers import router
from models.plant import Plant

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cookie Jar")
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "healthy"}
