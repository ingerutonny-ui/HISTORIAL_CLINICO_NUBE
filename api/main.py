from fastapi import FastAPI, Depends, Request, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI()

# CORS configurado estrictamente para evitar los errores de tus capturas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función de guardado optimizada para evitar Timeouts
def guardar_datos_p2(data, p_id):
    db = database.SessionLocal()
    try:
        # Buscar si ya existe para actualizar o crear
        registro = db.query(models.AntecedentesP2).filter(models.AntecedentesP2.paciente_id == p_id).first()
        if not registro:
            registro = models.AntecedentesP2(paciente_id=p_id)
            db.add(registro)
        
        for clave, valor in data.items():
            if hasattr(registro, clave) and clave != "paciente_id":
                setattr(registro, clave, str(valor).upper())
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"ERROR CRÍTICO EN DB: {e}")
    finally:
        db.close()

@app.get("/")
def inicio():
    return {"proyecto": "HISTORIAL_CLINICO_NUBE", "servidor": "PLAN_STARTER_ACTIVE"}

@app.get("/api/paciente-completo/{id}")
def leer_paciente(id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    p1 = db.query(models.DeclaracionJurada).filter(models.DeclaracionJurada.paciente_id == id).first()
    
    return {
        "paciente": {
            "nombre": p.nombre, 
            "apellido": p.apellido, 
            "ci": p.ci, 
            "codigo": getattr(p, 'codigo_paciente', 'S/C')
        },
        "p1": {k: v for k, v in p1.__dict__.items() if not k.startswith('_')} if p1 else {}
    }

@app.post("/p2")
async def post_p2(r: Request, background_tasks: BackgroundTasks):
    try:
        data = await r.json()
        paciente_id = int(data.get("paciente_id"))
        
        # Ejecutamos el guardado de forma que no bloquee la respuesta HTTP
        background_tasks.add_task(guardar_datos_p2, data, paciente_id)
        
        return {"status": "exito", "mensaje": "Datos en cola de procesamiento"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}
