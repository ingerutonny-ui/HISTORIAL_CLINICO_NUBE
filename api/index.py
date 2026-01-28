import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/pacientes', methods=['POST'])
def registrar_paciente():
    try:
        datos = request.json
        nombre = datos.get('nombre', '')
        apellido = datos.get('apellido', '')
        
        # Generar código: Iniciales + 4 números aleatorios
        iniciales = (nombre[0] if nombre else 'X') + (apellido[0] if apellido else 'X')
        numero_aleatorio = random.randint(1000, 9999)
        codigo_generado = f"{iniciales.upper()}{numero_aleatorio}"
        
        return jsonify({
            "mensaje": "PACIENTE REGISTRADO",
            "codigo": codigo_generado
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Requerido para Vercel
def handler(event, context):
    return app(event, context)
