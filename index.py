import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from vercel_blob import put, list_blobs

app = Flask(__name__)
CORS(app)

# Nombre del archivo en tu almacenamiento Blob
BLOB_FILENAME = "pacientes_datos.json"

@app.route('/api/pacientes', methods=['GET'])
def get_pacientes():
    try:
        all_blobs = list_blobs()
        target = next((b for b in all_blobs['blobs'] if b['pathname'] == BLOB_FILENAME), None)
        if target:
            r = requests.get(target['url'])
            return jsonify(r.json()), 200
        return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pacientes', methods=['POST'])
def add_paciente():
    try:
        data = request.json
        # 1. Obtener datos actuales
        all_blobs = list_blobs()
        target = next((b for b in all_blobs['blobs'] if b['pathname'] == BLOB_FILENAME), None)
        
        lista_actual = []
        if target:
            r = requests.get(target['url'])
            lista_actual = r.json()

        # 2. Crear el nuevo registro
        nuevo_paciente = {
            "id": len(lista_actual) + 1,
            "nombre": data.get('nombre'),
            "apellido": data.get('apellido'),
            "dni": data.get('dni')
        }
        lista_actual.append(nuevo_paciente)

        # 3. Guardar en la nube (addRandomSuffix: false es clave)
        put(BLOB_FILENAME, json.dumps(lista_actual), {
            "contentType": "application/json",
            "addRandomSuffix": "false"
        })
        
        return jsonify({"mensaje": "Registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Fallo: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
