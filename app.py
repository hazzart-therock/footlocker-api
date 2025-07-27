from flask import Flask, request, jsonify
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

    # 🔁 Simulación temporal: solo la talla "10.0" está disponible
    if talla == "10.0":
        resultado = {"disponible": True}
    else:
        resultado = {"disponible": False}

    return jsonify(resultado)

@app.route('/')
def index():
    return "Footlocker API is running"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render define esta variable automáticamente
    app.run(host="0.0.0.0", port=port)
