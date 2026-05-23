from fastapi import FastAPI, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import crud, models

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# Endpoints corregidos: Extraen el objeto interno ANTES de llamar al CRUD
@app.post("/p2/")
def registrar_p2(data: dict, db: Session = Depends(get_db)):
    # Si el frontend envía { "antecedentes": { ... } }, extraemos la parte interna
    content = data.get("antecedentes", data)
    return crud.upsert_p2(db, content)

@app.post("/p3/")
def registrar_p3(data: dict, db: Session = Depends(get_db)):
    # Si el frontend envía { "habitos": { ... } }, extraemos la parte interna
    content = data.get("habitos", data)
    return crud.upsert_p3(db, content)

# ... (El resto de tus rutas existentes aquí sin cambios) ...
