import requests
from bs4 import BeautifulSoup

def verificar_disponibilidad(url, talla):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except requests.RequestException:
        return {"disponible": False, "error": "Fallo al obtener la página"}

    try:
        soup = BeautifulSoup(res.text, 'html.parser')
        botones = soup.find_all('button', class_='SizeSelector-button-newDesign')

        for boton in botones:
            span = boton.find('span')
            texto = span.text.strip() if span else ""
            clases = boton.get('class', [])
            aria_label = boton.get('aria-label', '')

            if texto == talla:
                if 'SizeSelectorNewDesign-button--disabled' in clases or 'Sold Out' in aria_label:
                    return {"disponible": False}
                else:
                    return {"disponible": True}

        return {"disponible": False, "error": "Talla no encontrada"}

    except Exception as e:
        return {"disponible": False, "error": "Fallo al procesar HTML"}
