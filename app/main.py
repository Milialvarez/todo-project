from fastapi import FastAPI
from app.db.session import engine
from app.db import base

app = FastAPI()

# Crea las tablas automáticamente (solo mientras desarrollás)
base.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "API funcionando"}
