import logging
import os
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from logging import handlers

load_dotenv()

app = Flask(__name__)

# Configuración del logger para Windows Event Viewer
logger = logging.getLogger("PedidosServiceLogger")
logger.setLevel(logging.INFO)

# Crear un manejador para el Event Viewer
event_log_handler = handlers.NTEventLogHandler("PedidosService")
logger.addHandler(event_log_handler)

pedidos = [
    {"id": 1, "usuario_id": 1, "producto": "Laptop", "cantidad": 1, "total": 999.99},
    {"id": 2, "usuario_id": 1, "producto": "Mouse", "cantidad": 2, "total": 49.98},
    {"id": 3, "usuario_id": 2, "producto": "Monitor", "cantidad": 1, "total": 299.99},
    {"id": 4, "usuario_id": 3, "producto": "Teclado", "cantidad": 1, "total": 89.99}
]

def verificar_usuario(usuario_id):
    """Verifica si existe un usuario consultando al servicio de usuarios"""
    try:
        puerto_usuarios = int(os.getenv('USERS_SERVICE_PORT', 5000))
        response = requests.get(f'http://localhost:{puerto_usuarios}/api/usuarios/{usuario_id}')
        return response.status_code == 200
    except requests.RequestException:
        logger.error("Error al verificar el usuario con el servicio de usuarios")
        return False

@app.route('/api/pedidos', methods=['GET'])
def obtener_pedidos():
    """Endpoint para obtener todos los pedidos"""
    logger.info("Solicitud para obtener todos los pedidos")
    return jsonify({"pedidos": pedidos, "total": len(pedidos)})

@app.route('/api/pedidos/usuario/<int:usuario_id>', methods=['GET'])
def obtener_pedidos_usuario(usuario_id):
    """Endpoint para obtener los pedidos de un usuario específico"""
    if not verificar_usuario(usuario_id):
        logger.warning(f"Usuario {usuario_id} no encontrado al buscar pedidos")
        return jsonify({"error": "Usuario no encontrado"}), 404

    pedidos_usuario = [p for p in pedidos if p["usuario_id"] == usuario_id]
    logger.info(f"Pedidos encontrados para el usuario {usuario_id}")
    return jsonify({
        "usuario_id": usuario_id,
        "pedidos": pedidos_usuario,
        "total_pedidos": len(pedidos_usuario)
    })

@app.route('/health', methods=['GET'])
def healthcheck():
    """Endpoint para verificar el estado del servicio"""
    logger.info("Solicitud de verificación de salud del servicio de pedidos")
    return jsonify({"status": "healthy", "service": "pedidos"})

if __name__ == '__main__':
    puerto = int(os.getenv('ORDERS_SERVICE_PORT', 5001))
    logger.info("Iniciando servicio de pedidos")
    app.run(port=puerto, debug=True)
