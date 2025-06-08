import spacy
from pprint import pprint

# Cargar modelo de spaCy para español
nlp = spacy.load("es_core_news_sm")

def tokens_analyzer(texto: str, filtrar=True) -> dict:
    doc = nlp(texto)
    analisis = []
    singulares = []
    plurales = []
    masculinos = []
    femeninos = []

    for position, token in enumerate(doc):
        if filtrar and token.is_punct:
            continue

        genero = list(token.morph.get("Gender"))
        numero = list(token.morph.get("Number"))

        # Clasificación por número
        if "Sing" in numero:
            singulares.append(token.text)
        elif "Plur" in numero:
            plurales.append(token.text)

        # Clasificación por género
        if "Masc" in genero:
            masculinos.append(token.text)
        elif "Fem" in genero:
            femeninos.append(token.text)

        # Este analisis evalua token a token las propiedades del mismo
        analisis.append(
            {
                "Posicion": position,
                "Stopword": token.is_stop,
                "Palabra": token.text,
                "Lema": token.lemma_,
                "Gramatica": token.pos_,
                "Genero": genero,
                "Numero": numero,
            }
        )

    # Este resumen generaliza lo que se ha encontrado en el texto de acuerdo a las propiedades de cada token
    resumen = {
        "singulares": {"coincidencias": len(singulares), "palabras": singulares},
        "plurales": {"coincidencias": len(plurales), "palabras": plurales},
        "masculino": {"coincidencias": len(masculinos), "palabras": masculinos},
        "femenino": {"coincidencias": len(femeninos), "palabras": femeninos},
    }
    token_props = {"analisis": analisis, "resumen": resumen}

    return token_props

# Ejemplo de uso directo
if __name__ == "__main__":
    texto = "el perrito sureño de los cacahuates magicos"
    resultado = tokens_analyzer(texto)
    pprint(resultado["resumen"])
