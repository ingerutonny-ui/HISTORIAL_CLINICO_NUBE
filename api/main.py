from flask import Flask, jsonify, request
from .database import SessionLocal
from . import crud, schemas

app = Flask(__name__)

@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok", "message": "HISTORIAL_CLINICO_NUBE funcionando"})

@app.route('/api/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    db = SessionLocal()

    try:
        paciente_data = schemas.PacienteBase(**data)

        nuevo_paciente = crud.crear_paciente(
            db,
            nombre=paciente_data.nombre,
            apellido=paciente_data.apellido,
            ci=paciente_data.ci,
            fecha_ingreso=paciente_data.fechaIngreso,
            codigo=paciente_data.codigo
        )

        respuesta = schemas.PacienteResponse.from_orm(nuevo_paciente)
        return jsonify({"status": "ok", "mensaje": "Paciente registrado", "paciente": respuesta.dict()})
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)})
    finally:
        db.close()

# 🔧 Esta función permite que Vercel ejecute Flask como WSGI
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)
