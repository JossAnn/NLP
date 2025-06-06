import re
import string
from unidecode import unidecode


def clean_text(text: str) -> str:
    # Minusculizar
    text = text.lower()

    # Eliminar tildes y caracteres no ASCII
    text = unidecode(text)

    # Eliminar puntuación
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Eliminar caracteres no alfanuméricos (excepto espacios)
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # Eliminar múltiples espacios
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Para pruebas rápidas
if __name__ == "__main__":
    TEXTO = "¡El Perrito, sureño... de los cacahuates mágicos!"
    limpio = clean_text(TEXTO)
    print(f"Original: {TEXTO}")
    print(f"Limpio:   {limpio}")
