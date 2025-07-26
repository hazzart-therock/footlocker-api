import requests
from bs4 import BeautifulSoup
import traceback

def verificar_disponibilidad(url, talla):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except requests.RequestException:
        return {"status": "error", "message": "Fallo al obtener la página"}

    try:
        soup = BeautifulSoup(res.text, 'html.parser')
        botones = soup.find_all('button', class_='SizeSelector-button-newDesign')

        for boton in botones:
            span = boton.find('span')
            if span and span.text.strip() == talla:
                clases = boton.get('class', [])
                if 'SizeSelectorNewDesign-button--disabled' not in clases:
                    return {"status": "ok", "disponibilidad": "Disponible"}
                else:
                    return {"status": "ok", "disponibilidad": "Agotado"}

        return {"status": "ok", "disponibilidad": "Agotado"}

    except Exception:
        return {"status": "error", "message": "Fallo al procesar HTML"}