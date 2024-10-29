from flask import Flask, jsonify
import redis
import time

app = Flask(__name__)

# Conectar a Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

# Definir el endpoint /data
@app.route('/data', methods=['GET'])
def get_data():
    # Ejemplo de respuesta JSON
    data = {"mensaje": "Hola, mundo!", "status": "success"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
