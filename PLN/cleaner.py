import re
import string
from unidecode import unidecode


def clean_text(text: str) -> str:
    # Minusculizar
    text = text.lower()

    # Caso especial para mantener la letra ñ (reemplazandola)
    text = text.replace("ñ", "__enie__")
    
    # Eliminar tildes y caracteres no ASCII
    text = unidecode(text)

    # Restaurar la ñ (porque no es ASCII, pero en la fonetica sera evaluada)
    text = text.replace("__enie__", "ñ")
    
    # Eliminar puntuación
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Eliminar caracteres no alfanuméricos (excepto espacios)
    text = re.sub(r"[^a-z0-9ñ\s]", "", text)

    # Eliminar múltiples espacios
    text = re.sub(r"\s+", " ", text).strip()

    return text
