"""
Aplicación principal Flask
"""
from flask import Flask, send_from_directory, session
from flask_cors import CORS
import os

from database import init_db
from routes import api

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Habilitar CORS
CORS(app, supports_credentials=True)

# Registrar blueprint de API
app.register_blueprint(api)

# Ruta para servir archivos estáticos
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# La base de datos se inicializa al ejecutar el servidor

if __name__ == '__main__':
    # Asegurar que la base de datos existe
    init_db()
    
    print("=" * 50)
    print("Sistema de Gestión de Proyectos")
    print("=" * 50)
    print("Servidor iniciado en http://localhost:5000")
    print("Usuario administrador por defecto:")
    print("  Email: admin@proyectos.com")
    print("  Contraseña: admin123")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

