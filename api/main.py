from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/declaraciones/p1", response_model=schemas.DeclaracionJurada)
def save_declaracion_p1(declaracion: schemas.DeclaracionJuradaCreate, db: Session = Depends(get_db)):
    return crud.create_declaracion_p1(db=db, declaracion=declaracion)
