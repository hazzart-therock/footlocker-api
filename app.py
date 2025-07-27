from flask import Flask, request, jsonify
from scraper import verificar_disponibilidad
import os

app = Flask(__name__)

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json(force=True)
    print("📦 Datos recibidos:", data)

    url = data.get('url')
    talla = data.get('talla')

    if not url or not talla:
        return jsonify({"error": "Faltan parámetros"}), 400

    try:
        resultado = verificar_disponibilidad(url, talla)
        return jsonify(resultado)
    except Exception as e:
        print("❌ Error en verificar_disponibilidad:", e)
        return jsonify({"error": "Error interno en el scraper"}), 500

@app.route('/')
def index():
    return "Footlocker API is running"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render define esta variable automáticamente
    app.run(host="0.0.0.0", port=port)
