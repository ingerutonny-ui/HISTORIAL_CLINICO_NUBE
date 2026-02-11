# Este archivo redirige el tráfico a la aplicación principal de FastAPI
from .main import app

# Esto es lo que Render usará como punto de entrada
handler = app
