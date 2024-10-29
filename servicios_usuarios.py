import logging
import os
import win32api
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from logging import handlers

load_dotenv()

app = Flask(__name__)

# Configuración del logger para Windows Event Viewer
logger = logging.getLogger("UsuariosServiceLogger")
logger.setLevel(logging.INFO)

# Crear un manejador para el Event Viewer
event_log_handler = handlers.NTEventLogHandler("UsuariosService")
logger.addHandler(event_log_handler)

usuarios = [
    {"id": 1, "nombre": "Ana Garcia", "email": "ana@email.com"},
    {"id": 2, "nombre": "Carlos Lopez", "email": "carlos@email.com"},
    {"id": 3, "nombre": "Maria Rodriguez", "email": "maria@email.com"}
]

def obtener_usuario_actual():
    """Obtiene el nombre de usuario actual en Windows"""
    try:
        return win32api.GetUserName()
    except Exception as e:
        logger.error(f"Error al obtener el usuario actual: {e}")
        return None

@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    """Endpoint para obtener todos los usuarios"""
    usuario_actual = obtener_usuario_actual()
    logger.info(f"Solicitud para obtener todos los usuarios por {usuario_actual}")
    return jsonify({"usuarios": usuarios, "total": len(usuarios)})

@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    """Endpoint para obtener un usuario específico por ID"""
    usuario_actual = obtener_usuario_actual()
    usuario = next((u for u in usuarios if u["id"] == usuario_id), None)
    if usuario:
        logger.info(f"Usuario {usuario_id} encontrado por {usuario_actual}")
        return jsonify({"usuario": usuario})
    logger.warning(f"Usuario {usuario_id} no encontrado, solicitud por {usuario_actual}")
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/health', methods=['GET'])
def healthcheck():
    """Endpoint para verificar el estado del servicio"""
    logger.info("Solicitud de verificación de salud del servicio de usuarios")
    return jsonify({"status": "healthy", "service": "usuarios"})

if __name__ == '__main__':
    puerto = int(os.getenv('USERS_SERVICE_PORT', 5000))
    logger.info("Iniciando servicio de usuarios")
    app.run(port=puerto, debug=True)
