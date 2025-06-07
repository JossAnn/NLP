from pprint import pprint
from cleaner import clean_text
from transliterator import transliterador


def comparador(texto_a: str, texto_b: str):# -> dict:

    texto_trans_a = transliterador(texto_a)
    texto_a_limpio = clean_text(texto_trans_a)
    texto_trans_b = transliterador(texto_b)
    texto_b_limpio = clean_text(texto_trans_b)

    # Ejemplo de salida Final
    # {
    #    "similitud_fonetica": "85%",
    #    "sinonimos":   {"coincidencias": 2, "palabras": [  ["sureño", "mágica"],
    #                                                       ["cacahuates", "almohada"]  ],  "peso": 0.2},
    #    "antonimos":   {"coincidencias": 0, "palabras": [],                                "peso": 0},
    #    "singulares":  {"coincidencias": 1, "palabras": ["perrito"],                       "peso": 0.1},
    #    "plurales":    {"coincidencias": 1, "palabras": ["cacahuates"],                    "peso": 0.1},
    #    "masculino":   {"coincidencias": 1, "palabras": ["perrito"],                       "peso": 0.1},
    #    "femenino":    {"coincidencias": 1, "palabras": ["almohada"],                      "peso": 0.1},
    #    "transliteraciones":   [   ["perrito", "p3rr1t0"],
    #                               ["sureño", "sureno"]    ]
    # }
    salida_final = {
        "texto_a": texto_a,
        "texto_a_limpio": texto_a_limpio,
        "texto_b": texto_b,
        "texto_b_limpio": texto_b_limpio,
    }
    return salida_final

if __name__ == "__main__":
    texto1 = "3l perr1t0 5ureño de lo5 38 cacaHu4tes"
    texto2 = "Las 23 almohadas mág1cas del perrito cAc4huater0"
    resultados = comparador(texto1, texto2)
    

    pprint(resultados)
