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

            # Verifica si el texto coincide con la talla
            if texto == talla:
                # Verifica si está deshabilitado
                if 'SizeSelectorNewDesign-button--disabled' in clases or boton.has_attr('disabled'):
                    return {"disponible": False}
                else:
                    return {"disponible": True}

        # Si no se encontró la talla en el HTML
        return {"disponible": False, "error": "Talla no encontrada"}

    except Exception as e:
        return {"disponible": False, "error": "Fallo al procesar HTML"}
