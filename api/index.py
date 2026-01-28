import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Habilitamos CORS para que el index.html pueda hablar con este código
CORS(app)

# Ubicación permitida para escribir en la nube de Vercel
DB_PATH = '/tmp/pacientes.db'

def init_db():
    """Crea la tabla si no existe al iniciar la aplicación"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            dni TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ejecutamos la creación de la tabla cada vez que el servidor despierta
init_db()

@app.route('/api/pacientes', methods=['POST'])
def agregar_paciente():
    try:
        data = request.json
        # Extraemos los datos enviados desde el formulario
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        dni = data.get('dni')

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO pacientes (nombre, apellido, dni) VALUES (?, ?, ?)',
                       (nombre, apellido, dni))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Paciente guardado"}), 201
    except Exception as e:
        # Si algo falla, el servidor nos dirá exactamente qué pasó
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/pacientes', methods=['GET'])
def obtener_pacientes():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pacientes')
        rows = cursor.fetchall()
        conn.close()
        
        # Convertimos los datos de la base de datos a formato JSON
        pacientes = []
        for p in rows:
            pacientes.append({
                "id": p[0],
                "nombre": p[1],
                "apellido": p[2],
                "dni": p[3]
            })
        return jsonify(pacientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Esta parte es necesaria para el entorno local y Vercel
if __name__ == '__main__':
    app.run(debug=True)
