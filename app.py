from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import verificar_disponibilidad  # Asegúrate de que esta función esté bien definida

app = Flask(__name__)

# Permitir solicitudes desde tu dominio principal y con www
CORS(app, resources={r"/check": {"origins": [
    "https://therocksport.com",
    "https://www.therocksport.com"
]}})

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json(force=True)
    print("📦 Datos recibidos:", data)

    url = data.get('url')
    talla = data.get('talla')

    if not url or not talla:
        return jsonify({"disponible": False, "error": "Faltan parámetros"}), 400

    try:
        resultado = verificar_disponibilidad(url, talla)
        return jsonify(resultado)
    except Exception as e:
        print("❌ Error en verificar_disponibilidad:", e)
        return jsonify({"disponible": False, "error": "Error interno en el scraper"}), 500

@app.route('/')
def index():
    return "Footlocker API is running"
