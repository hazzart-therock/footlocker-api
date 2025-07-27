import requests
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.INFO)

def verificar_disponibilidad(url, talla):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    for intento in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            break
        except requests.RequestException as e:
            logging.warning(f"Intento {intento+1} fallido: {e}")
            time.sleep(2)
    else:
        return {"disponible": False, "error": "Fallo al obtener la página"}

    try:
        soup = BeautifulSoup(res.text, 'html.parser')

        # Selector principal
        botones = soup.find_all("button", attrs={"data-qa": "size-button"})

        # Fallback si no se encuentra nada
        if not botones:
            botones = soup.select("button[aria-label*='Size']")

        if not botones:
            with open("error_snapshot.html", "w", encoding="utf-8") as f:
                f.write(res.text)
            return {"disponible": False, "error": "Botones de talla no encontrados"}

        for boton in botones:
            texto = boton.get_text(strip=True)
            clases = boton.get("class", [])
            aria_label = boton.get("aria-label", "")

            # Comparación flexible
            if talla.strip() in texto.strip():
                if "disabled" in clases or "Sold Out" in aria_label:
                    return {"disponible": False}
                else:
                    return {"disponible": True}

        return {"disponible": False, "error": "Talla no encontrada"}

    except Exception as e:
        with open("error_snapshot.html", "w", encoding="utf-8") as f:
            f.write(res.text)
        return {"disponible": False, "error": "Fallo al procesar HTML"}
