from fastapi import FastAPI
from api.database import SessionLocal  # Cambiamos .database por api.database

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API HISTORIAL_CLINICO_NUBE funcionando"}

@app.get("/healthz")
def health_check():
    try:
        db = SessionLocal()
        # Usamos text() de sqlalchemy para que la consulta sea válida
        from sqlalchemy import text
        db.execute(text("SELECT 1")) 
        db.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
