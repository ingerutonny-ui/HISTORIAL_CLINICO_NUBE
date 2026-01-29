from flask import Flask, jsonify, request
from .database import SessionLocal
from . import crud

app = Flask(__name__)

@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok", "message": "HISTORIAL_CLINICO_NUBE funcionando"})

@app.route('/api/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    db = SessionLocal()

    try:
        nuevo_paciente = crud.crear_paciente(
            db,
            nombre=data.get("nombre"),
            apellido=data.get("apellido"),
            dni=data.get("dni"),
            fecha_ingreso=data.get("fechaIngreso"),
            codigo=data.get("codigo")
        )
        return jsonify({"status": "ok", "mensaje": "Paciente registrado", "paciente": {
            "id": nuevo_paciente.id,
            "nombre": nuevo_paciente.nombre,
            "apellido": nuevo_paciente.apellido,
            "dni": nuevo_paciente.dni,
            "fecha_ingreso": nuevo_paciente.fecha_ingreso,
            "codigo": nuevo_paciente.codigo
        }})
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)})
    finally:
        db.close()

def handler(request):
    return app(request)
