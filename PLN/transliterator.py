def transliterador(texto: str) -> str:
    reemplazos = {
        "0": "o",
        "1": "i",
        "2": "z",
        "3": "e",
        "4": "a",
        "5": "s",
        "6": "b",
        "7": "t",
        "8": "b",
        "9": "g",
    }

    def normalizar_palabra(palabra: str) -> str:
        # Si es un número puro, no cambiar
        if palabra.isdigit():
            return palabra

        # Si mezcla letras y números, reemplazar solo los números por letras
        return "".join(reemplazos.get(c, c) for c in palabra.lower())

    palabras = texto.split()
    palabras_normalizadas = [normalizar_palabra(p) for p in palabras]
    return " ".join(palabras_normalizadas)