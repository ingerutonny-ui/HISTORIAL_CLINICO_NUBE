import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from vercel_blob import put, list_blobs

app = Flask(__name__)
CORS(app)

# Nombre del archivo que se creará en tu Storage Blob
BLOB_FILENAME = "pacientes_datos.json"

@app.route('/api/pacientes', methods=['GET'])
def get_pacientes():
    try:
        # 1. Listamos los archivos en el Blob para ver si el JSON ya existe
        all_blobs = list_blobs()
        target = next((b for b in all_blobs['blobs'] if b['pathname'] == BLOB_FILENAME), None)
        
        if target:
            # 2. Si existe, leemos los datos desde su URL pública
            r = requests.get(target['url'])
            return jsonify(r.json()), 200
        
        # Si no existe todavía, devolvemos una lista vacía
        return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pacientes', methods=['POST'])
def add_paciente():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Faltan datos"}), 400

        # 1. Buscamos si ya hay pacientes guardados para no borrarlos
        all_blobs = list_blobs()
        target = next((b for b in all_blobs['blobs'] if b['pathname'] == BLOB_FILENAME), None)
        
        lista_actual = []
        if target:
            r = requests.get(target['url'])
            lista_actual = r.json()

        # 2. Creamos el nuevo registro
        nuevo_paciente = {
            "id": len(lista_actual) + 1,
            "nombre": data.get('nombre'),
            "apellido": data.get('apellido'),
            "dni": data.get('dni')
        }
        lista_actual.append(nuevo_paciente)

        # 3. Guardamos la lista completa de nuevo en el Blob
        # IMPORTANTE: 'addRandomSuffix': 'false' mantiene el nombre del archivo fijo
        put(BLOB_FILENAME, json.dumps(lista_actual), {
            "contentType": "application/json",
            "addRandomSuffix": "false"
        })
        
        return jsonify({"mensaje": "✅ Registrado exitosamente en la nube"}), 201
    except Exception as e:
        return jsonify({"error": f"Fallo de conexión al Blob: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
