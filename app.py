from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# ✅ CORS global para permitir solicitudes desde tu dominio
CORS(app, origins=[
    "https://therocksport.com",
    "https://www.therocksport.com"
])

# 🟢 Ruta de prueba para verificar conectividad
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "✅ API activa", "message": "pong"})

# 🔍 Ruta principal para verificar disponibilidad
@app.route("/check", methods=["POST"])
def check():
    print("✅ Solicitud recibida en /check")

    try:
        data = request.get_json()
        print("📦 Datos recibidos:", data)

        url = data.get("url")
        talla = data.get("talla")

        if not url or not talla:
            return jsonify({"error": "Faltan parámetros"}), 400

        # 🧪 Simulación de scraping o verificación real
        # Aquí puedes integrar tu lógica real de scraping
        disponible = "footlocker" in url and talla in ["10", "10.5", "11"]

        print(f"🔎 Verificando talla {talla} en {url} → {'Disponible' if disponible else 'No disponible'}")

        return jsonify({
            "disponible": disponible,
            "talla": talla,
            "url": url
        })

    except Exception as e:
        print("❌ Error interno:", str(e))
        return jsonify({"error": "Error interno"}), 500

# 🟢 Ruta raíz para confirmar que el backend está activo
@app.route("/", methods=["GET"])
def home():
    return "✅ Footlocker API is running"

# 🚀 Ejecutar la app
if __name__ == "__main__":
    app.run(debug=True)
