import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Usamos una ruta temporal absoluta para evitar bloqueos de permisos
DB_PATH = "/tmp/historial.db"

def init_db():
    """Inicializa la base de datos desde cero en cada despliegue"""
    try:
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
    except Exception as e:
        print(f"Error inicializando DB: {e}")

# Llamamos a la creación de la tabla
init_db()

@app.route('/api/pacientes', methods=['GET'])
def get_pacientes():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pacientes')
        rows = cursor.fetchall()
        conn.close()
        return jsonify([{"id": r[0], "nombre": r[1], "apellido": r[2], "dni": r[3]} for r in rows]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pacientes', methods=['POST'])
def add_paciente():
    try:
        data = request.json
        # Verificamos que lleguen los datos para evitar errores de servidor
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO pacientes (nombre, apellido, dni) VALUES (?, ?, ?)',
                       (data.get('nombre'), data.get('apellido'), data.get('dni')))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "✅ Registrado con éxito"}), 201
    except Exception as e:
        # Esto nos enviará el error real al navegador si algo falla
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
