from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok", "message": "HISTORIAL_CLINICO_NUBE funcionando"})

# Esto es necesario para que Vercel lo detecte
def handler(request):
    return app(request)
