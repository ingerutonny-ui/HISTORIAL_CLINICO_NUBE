from http.server import BaseHTTPRequestHandler
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

# 🔧 Adaptador oficial para Vercel Functions
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/healthcheck":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok","message":"HISTORIAL_CLINICO_NUBE funcionando"}')
        else:
            self.send_response(404)
            self.end_headers()
