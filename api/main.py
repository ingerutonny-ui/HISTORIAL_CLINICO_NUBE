from fastapi import FastAPI
from .database import SessionLocal

app = FastAPI()

@app.get("/healthz")
def health_check():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")  # consulta mínima
        db.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
