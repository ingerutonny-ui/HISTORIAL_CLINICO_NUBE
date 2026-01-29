from fastapi import FastAPI
from sqlalchemy import text
from api.database import SessionLocal # Importación absoluta

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Proyecto HISTORIAL_CLINICO_NUBE en linea"}

@app.get("/healthz")
def health_check():
    db = SessionLocal()
    try:
        # Verificamos la conexión a PostgreSQL
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
    finally:
        db.close()
