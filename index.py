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
        nombre = datos.get('nombre', '').strip()
        apellido = datos.get('apellido', '').strip()
        
        # Lógica exacta para la imagen: Primera letra de Nombre + Primera de Apellido
        # Si falta alguno, usamos 'X' para evitar errores.
        in_n = nombre[0].upper() if nombre else 'X'
        in_a = apellido[0].upper() if apellido else 'X'
        
        # Generar 4 números aleatorios (ej. 6055)
        num = random.randint(1000, 9999)
        
        codigo_final = f"{in_n}{in_a}{num}"
        
        return jsonify({
            "mensaje": "PACIENTE REGISTRADO",
            "codigo": codigo_final
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Manejador para Vercel
def handler(event, context):
    return app(event, context)
