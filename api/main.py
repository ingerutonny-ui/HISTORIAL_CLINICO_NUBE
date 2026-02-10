from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database, crud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Intentar crear tablas al iniciar
try:
    models.Base.metadata.create_all(bind=database.engine)
except Exception as e:
    print(f"Error de conexión inicial: {e}")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/pacientes/")
def listar_pacientes(db: Session = Depends(get_db)):
    try:
        return crud.get_pacientes(db)
    except Exception as e:
        # Esto mostrará el error real en la consola del navegador
        raise HTTPException(status_code=500, detail=str(e))

# ... resto de tus endpoints de guardado (P1, P2, P3)
