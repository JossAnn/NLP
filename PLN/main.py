from pprint import pprint
from cleaner import clean_text
from transliterator import transliterator
from tokenizer import tokens_analyzer


def comparador(texto_a: str, texto_b: str):# -> dict:

    translit_a = transliterator(texto_a)  # El transliterador devuelve un objeto json, clean_text solo necesita "text_trans"
    translit_b = transliterator(texto_b)
    
    clean_a = clean_text(translit_a["text_trans"]) # clean_text espera una cadena de texto
    clean_b = clean_text(translit_b["text_trans"])
    
    tokeni_a = tokens_analyzer(clean_a)
    tokeni_b = tokens_analyzer(clean_b)
    
    salida_final = {
        #    "similitud_fonetica": "85%",
        #    "sinonimos":   {"coincidencias": 2, "palabras": [  ["sureño", "mágica"], ["cacahuates", "almohada"]  ],  "peso": 0.2},
        #    "antonimos":   {"coincidencias": 0, "palabras": [],                                "peso": 0},
        #    "singulares":  {"coincidencias": 1, "palabras": ["perrito"],                       "peso": 0.1},
        #    "plurales":    {"coincidencias": 1, "palabras": ["cacahuates"],                    "peso": 0.1},
        #    "masculino":   {"coincidencias": 1, "palabras": ["perrito"],                       "peso": 0.1},
        #    "femenino":    {"coincidencias": 1, "palabras": ["almohada"],                      "peso": 0.1},
        "tokeni_a": tokeni_a["resumen"],
        "tokeni_b": tokeni_b["resumen"],
        "transliteraciones": {
            "total": (int(translit_a["num_trans"]) + int(translit_b["num_trans"])),
            "texto1": translit_a["words_trans"], 
            "texto2": translit_b["words_trans"],
            }
    }
    return salida_final

if __name__ == "__main__":
    texto1 = "3l perr1t0 5ureño de lo5 38 cacaHu4tes"
    texto2 = "Las 23 almohadas mág1cas del perrote cAc4huater0"
    resultados = comparador(texto1, texto2)
    

    pprint(resultados)
