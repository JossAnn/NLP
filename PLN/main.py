from pprint import pprint
from cleaner import clean_text
from transliterator import transliterator
from tokenizer import tokens_analyzer
from phonetic_evaluator import evalue_phonetic


def comparador(texto_a: str, texto_b: str):# -> dict:

    translit_a = transliterator(texto_a)  # El transliterador devuelve un objeto json, clean_text solo necesita "text_trans"
    translit_b = transliterator(texto_b)

    clean_a = clean_text(translit_a["text_trans"]) # clean_text espera una cadena de texto
    clean_b = clean_text(translit_b["text_trans"])

    tokeni_a = tokens_analyzer(clean_a)
    tokeni_b = tokens_analyzer(clean_b)

    evaluation = evalue_phonetic(tokeni_a, tokeni_b)

    salida_final = {
        "similitud_fonetica": float(evaluation["similitud"]),
        "similitud_ponderada": float(evaluation["simi_pond"]),
    #}
    #"""
        "antonimos_num": evaluation["antonimos"]["coincidencias"],
        "antonimos": evaluation["antonimos"]["palabras"],
        "antonimos_peso": evaluation["antonimos"]["peso"],
        "sinonimos_num": evaluation["sinonimos"]["coincidencias"],
        "sinonimos": evaluation["sinonimos"]["palabras"],
        "sinonimos_peso": evaluation["sinonimos"]["peso"],
        "texto_a_fem_num": tokeni_a["resumen"]["femenino"]["coincidencias"],
        "texto_a_femeninos": tokeni_a["resumen"]["femenino"]["palabras"],
        "texto_a_masc_num": tokeni_a["resumen"]["masculino"]["coincidencias"],
        "texto_a_masculinos": tokeni_a["resumen"]["masculino"]["palabras"],
        "texto_a_plur_num": tokeni_a["resumen"]["plurales"]["coincidencias"],
        "texto_a_plurales": tokeni_a["resumen"]["plurales"]["palabras"],
        "texto_a_sing_num": tokeni_a["resumen"]["singulares"]["coincidencias"],
        "texto_a_sungulares": tokeni_a["resumen"]["singulares"]["palabras"],
        "texto_b_fem_num": tokeni_b["resumen"]["femenino"]["coincidencias"],
        "texto_b_femeninos": tokeni_b["resumen"]["femenino"]["palabras"],
        "texto_b_masc_num": tokeni_b["resumen"]["masculino"]["coincidencias"],
        "texto_b_masculinos": tokeni_b["resumen"]["masculino"]["palabras"],
        "texto_b_plur_num": tokeni_b["resumen"]["plurales"]["coincidencias"],
        "texto_b_plurales": tokeni_b["resumen"]["plurales"]["palabras"],
        "texto_b_sing_num": tokeni_b["resumen"]["singulares"]["coincidencias"],
        "texto_b_sungulares": tokeni_b["resumen"]["singulares"]["palabras"],
        "original_text_a": texto_a,
        "original_text_b": texto_b,
        "translit_text_a": translit_a["text_trans"],
        "translit_words_a": translit_a["words_trans"],
        "translit_a_total": int(translit_a["num_trans"]),
        "translit_text_b": translit_b["text_trans"],
        "translit_words_b": translit_b["words_trans"],
        "translit_b_total": int(translit_b["num_trans"]),
    }
    #"""
    return salida_final

if __name__ == "__main__":
    texto1 = "Ingrese el texto uno"
    texto2 = "N0 1mPor74 c0m0 L0 35cr1B45"
    resultados = comparador(texto1, texto2)

    pprint(resultados)
