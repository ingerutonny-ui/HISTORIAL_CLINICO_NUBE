from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database

# Iniciar la base de datos en el DISK persistente
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configuración de seguridad CORS
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

@app.get("/")
def health_check():
    return {"status": "ok", "storage": "DISK", "project": "HISTORIAL_CLINICO_NUBE"}

# --- RUTA 1: REGISTRO DE PACIENTE ---
@app.post("/pacientes/")
async def create_paciente(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    db_obj = models.Paciente(
        nombre=data.get("nombre"),
        apellido=data.get("apellido"),
        ci=data.get("ci"),
        codigo_paciente=data.get("codigo_paciente")
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# --- RUTA 2: PARTE 1 (FILIACIÓN) ---
@app.post("/filiacion/")
async def create_filiacion(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    db_obj = models.DeclaracionJurada(
        paciente_id=data.get("paciente_id"),
        edad=data.get("edad"),
        sexo=data.get("sexo"),
        fecha_nacimiento=data.get("fecha_nacimiento"),
        lugar_nacimiento=data.get("lugar_nacimiento"),
        domicilio=data.get("domicilio"),
        n_casa=data.get("n_casa"),
        zona_barrio=data.get("zona_barrio"),
        ciudad=data.get("ciudad"),
        pais=data.get("pais"),
        telefono=data.get("telefono"),
        estado_civil=data.get("estado_civil"),
        profesion_oficio=data.get("profesion_oficio")
    )
    db.add(db_obj)
    db.commit()
    return {"status": "success", "step": "P1_COMPLETED"}

# --- RUTA 3: PARTE 2 (ANTECEDENTES - LOS 22 CAMPOS) ---
@app.post("/declaraciones/p2/")
async def create_p2(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        # Mapeo explícito para asegurar que cada uno de los 22 campos se guarde
        db_obj = models.AntecedentesP2(
            paciente_id=data.get("paciente_id"),
            vista=data.get("vista"),
            auditivo=data.get("auditivo"),
            respiratorio=data.get("respiratorio"),
            cardio=data.get("cardio"),
            digestivos=data.get("digestivos"),
            sangre=data.get("sangre"),
            genitourinario=data.get("genitourinario"),
            sistema_nervioso=data.get("sistema_nervioso"),
            psiquiatricos=data.get("psiquiatricos"),
            osteomusculares=data.get("osteomusculares"),
            reumatologicos=data.get("reumatologicos"),
            dermatologicas=data.get("dermatologicas"),
            alergias=data.get("alergias"),
            cirugias=data.get("cirugias"),
            infecciones=data.get("infecciones"),
            acc_personales=data.get("acc_personales"),
            acc_trabajo=data.get("acc_trabajo"),
            medicamentos=data.get("medicamentos"),
            endocrino=data.get("endocrino"),
            familiares=data.get("familiares"),
            otros_especificos=data.get("otros_especificos"),
            generales=data.get("generales")
        )
        db.add(db_obj)
        db.commit()
        return {"status": "success", "message": "P2 guardada correctamente"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "detail": str(e)}

# --- RUTA 4: CONSULTA (PARA EL BOTÓN DE VER BASE DE DATOS) ---
@app.get("/pacientes/")
def get_all_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
