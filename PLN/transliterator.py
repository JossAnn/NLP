def transliterator(texto: str) -> object:
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

    transliteraciones = []

    # Minusculizar y dividir el texto
    texto = texto.lower()
    palabras_entrada = texto.split()

    def transliterar_palabras(palabra: str) -> str:
        # Si es un número puro, no cambiar
        if palabra.isdigit():
            return palabra

        # Si mezcla letras y números, reemplazar solo los números por letras
        return "".join(reemplazos.get(letra, letra) for letra in palabra.lower())

    # Transliteración
    palabras_transli = [transliterar_palabras(palabra) for palabra in palabras_entrada]
    texto_transliterado = " ".join(palabras_transli)

    # Es una lista emparejada de posiciones en las listas si las palabras son diferentes
    transliteraciones = [(origial, translit) for origial, translit in zip(palabras_entrada, palabras_transli) if origial != translit]
    #transliteraciones = [(origial, translit) for origial, translit in zip(palabras_entrada, palabras_transli)] # Sin el filtro devuelve ambas listas relacionadas
    translit_props = {
        "origin_text": texto,
        "text_trans": texto_transliterado,
        "num_trans": len(transliteraciones),
        "words_trans": transliteraciones
    }
    return translit_props

"""
if __name__ == "__main__":
    texto = "3l perr1t0 mal0 5ureño de lo5 38 cacaHu4tes"
    print(transliterator(texto))
"""
