from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Cargar la configuración desde el archivo config.json
def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

configuracion = cargar_configuracion()

@app.route('/api/config', methods=['GET'])
def obtener_configuracion():
    """Endpoint para obtener la configuración actual."""
    return jsonify(configuracion)

@app.route('/api/config', methods=['PUT'])
def actualizar_configuracion():
    """Endpoint para actualizar la configuración."""
    nueva_config = request.json
    configuracion.update(nueva_config)
    
    # Guardar la nueva configuración en el archivo
    with open('config.json', 'w') as f:
        json.dump(configuracion, f, indent=4)

    return jsonify(configuracion)

@app.route('/health', methods=['GET'])
def healthcheck():
    """Endpoint para verificar el estado del servicio."""
    return jsonify({"status": "healthy", "service": configuracion['service_name']})

if __name__ == '__main__':
    puerto = 5000  # Puedes cambiar esto o hacerlo configurable
    app.run(port=puerto, debug=True)
