import spacy
# import warnings
from typing import Dict, List, Tuple
import numpy as np
# from pprint import pprint

# Suprimir advertencias de spaCy
# warnings.filterwarnings("ignore")

class AdvancedPhoneticEvaluator:
    def __init__(self):
        try:
            # Intentar cargar modelo grande primero, luego mediano, pequeño y basico (puro codigo) si no se encuentra ninguno
            try:
                self.nlp = spacy.load("es_core_news_lg")
                self.has_vectors = True
            except OSError:
                self.nlp = spacy.load("es_core_news_md")
                self.has_vectors = True
        except OSError:
            try:
                self.nlp = spacy.load("es_core_news_sm")
                self.has_vectors = False
                print("Usando modelo pequeño sin vectores. Instala: python -m spacy download es_core_news_md")
            except OSError:
                raise Exception("No se encontró ningun modelo de spaCy. Instala: python -m spacy download es_core_news_md")

        # Mapeo fonético (solo respaldo)
        self.phonetic_rules = {
            "b": "b",
            "v": "b",
            "c": "k",
            "k": "k",
            "q": "k",
            "z": "s",
            "s": "s",
            "g": "g",
            "j": "h",
            "y": "i",
            "ll": "i",
            "h": "",  # h muda
        }

        # Umbrales para clasificación semántica
        self.umb_sinon = 0.5  # Similitud media-alta = sinonimos
        self.umb_anton_min = 0.3  # Similitud muy baja
        self.umb_anton_max = 0.5  # Pero no demasiado alta

        # Diccionarios locales/regionales
        # De ser necesario, habrá que agregar jergas y mexicanadas
        """self.antonimos_conocidos = {
            "bueno": ["malo", "mala", "terrible", "horrible", "malvado", "pésimo"],
            "malo": ["bueno", "buena", "excelente", "magnifico", "genial", "perfecto"],
            "grande": ["pequeño", "diminuto", "minúsculo", "chico"],
            "pequeño": ["grande", "enorme", "gigante", "inmenso", "colosal"],
            "buena": ["mala", "terrible", "horrible", "pésima"],
            "mala": ["buena", "excelente", "magnifica", "genial", "perfecta"],
            "alto": ["bajo", "corto", "pequeño"],
            "bajo": ["alto", "elevado", "grande"],
        }
        self.sinonimos_conocidos = {
            "cahorra": ["perra", "cachorrita", "perrita", "perro", "perrito", "can", "chucho"],
            "perra": ["cahorra", "cachorrita", "perrita", "can", "chucha"],
            "perro": ["cahorro", "cachorrito", "perrito", "can", "chucho"],
            "perrito": ["cahorro", "cachorrito", "perro", "can", "chucho"],
            "can": ["perro", "perrita", "cahorra", "chucho"],
            "chucho": ["perro", "perrita", "cahorra", "can"],
            "gato": ["minino", "michi", "felino"],
            "minino": ["gato", "michi", "felino"],
            "casa": ["hogar", "vivienda", "domicilio"],
            "hogar": ["casa", "vivienda", "domicilio"],
            "surenio": ["sureño", "sureña"],
        }"""

        self.antonimos_dict = {
            "bueno": ["mal", "malo", "mala", "terrible", "horrible", "malvado", "pésimo"],
            "malo": ["bien", "buen", "bueno", "buena", "excelente", "magnifico", "genial", "perfecto"],
            "buen": ["mal", "malo", "mala", "terrible", "horrible", "malvado", "pésimo", "pésima"],
            "bien": ["mal", "malo", "mala", "terrible", "horrible", "malvado", "pésimo", "pésima"],
            "mal": ["bien", "buen", "buena", "bueno", "excelente", "magnifica", "genial", "perfecta", "perfecto"],
            "grande": ["pequeño", "diminuto", "minúsculo", "chico"],
            "pequeño": ["grande", "enorme", "gigante", "inmenso", "colosal"],
            "buena": ["mal", "mala", "malo", "terrible", "horrible", "pésima"],
            "mala": ["bien", "buen", "buena", "bueno", "excelente", "magnifica", "genial", "perfecta"],
            "alto": ["bajo", "corto", "pequeño"],
            "bajo": ["alto", "elevado", "grande"],
            "feliz": ["triste", "deprimido", "infeliz", "melancólico"],
            "triste": ["feliz", "alegre", "contento", "entusiasta"],
            "rápido": ["lento", "pausado", "despacio", "tardado"],
            "lento": ["rápido", "veloz", "ágil", "acelerado"],
            "fuerte": ["débil", "frágil", "endeble"],
            "débil": ["fuerte", "resistente", "robusto"],
            "nuevo": ["viejo", "antiguo", "usado"],
            "viejo": ["nuevo", "moderno", "reciente"],
            "limpio": ["sucio", "manchado", "contaminado"],
            "sucio": ["limpio", "aseado", "pulcro"],
            "amable": ["grosero", "descortés", "antipático", "rudo"],
            "rico": ["pobre", "necesitado", "modesto"],
            "pobre": ["rico", "adinerado", "acaudalado"],
            "fácil": ["difícil", "complejo", "complicado"],
            "difícil": ["fácil", "simple", "sencillo"],
            "oscuro": ["claro", "luminoso", "brillante"],
            "claro": ["oscuro", "tenue", "apagado"],
            "frío": ["caliente", "templado", "tibio"],
            "caliente": ["frío", "helado", "fresco"],
            "corto": ["largo", "extenso", "prolongado"],
            "largo": ["corto", "breve", "conciso"],
            "alegre": ["triste", "melancólico", "apagado"],
            "duro": ["blando", "suave", "delicado"],
            "blando": ["duro", "firme", "resistente"],
        }

        self.sinonimos_dict = {
            "cahorra": [
                "perra",
                "cachorrita",
                "perrita",
                "perro",
                "perrito",
                "can",
                "chucho",
            ],
            "perra": ["cahorra", "cachorrita", "perrita", "can", "chucha"],
            "perro": ["cahorro", "cachorrito", "perrito", "can", "chucho"],
            "perrito": ["cahorro", "cachorrito", "perro", "can", "chucho"],
            "can": ["perro", "perrita", "cahorra", "chucho"],
            "chucho": ["perro", "perrita", "cahorra", "can"],
            "gato": ["minino", "michi", "felino", "gatito"],
            "minino": ["gato", "michi", "felino"],
            "michi": ["gato", "minino", "felino"],
            "felino": ["gato", "minino", "michi"],
            "gatito": ["gato", "minino", "michi"],
            "casa": ["hogar", "vivienda", "domicilio", "residencia", "morada"],
            "hogar": ["casa", "vivienda", "domicilio"],
            "vivienda": ["casa", "hogar", "domicilio"],
            "domicilio": ["casa", "hogar", "vivienda"],
            "residencia": ["casa", "hogar", "morada"],
            "morada": ["casa", "hogar", "residencia"],
            "surenio": ["sureño", "sureña"],
            "sureño": ["surenio", "sureña"],
            "sureña": ["surenio", "sureño"],
            "auto": ["coche", "carro", "vehículo"],
            "coche": ["auto", "carro", "vehículo"],
            "carro": ["auto", "coche", "vehículo"],
            "vehículo": ["auto", "coche", "carro"],
            "niño": ["infante", "chico", "crío", "pequeño"],
            "niña": ["infanta", "chica", "cría", "pequeña"],
            "bonito": ["hermoso", "bello", "lindo", "precioso"],
            "bonita": ["hermosa", "bella", "linda", "preciosa"],
            "feliz": ["contento", "alegre", "satisfecho", "gozoso"],
            "contento": ["feliz", "alegre", "satisfecho"],
            "alegre": ["feliz", "contento", "jovial"],
            "silla": ["asiento", "butaca", "banco"],
            "mesa": ["tablón", "escritorio", "mueble"],
            "caminar": ["andar", "marchar", "pasear"],
            "comer": ["alimentarse", "devorar", "ingerir"],
            "beber": ["tomar", "sorber", "ingerir"],
        }

    def basic_phonetic_evaluation(self, tkn_a: str, tkn_b: str) -> float:
        # Similitud fonética básica como respaldo

        def to_phonetic(token):
            token = token.lower()
            result = ""
            for char in token:
                result += self.phonetic_rules.get(char, char)
            return result

        phonet_word_a, phonet_word_b = to_phonetic(tkn_a), to_phonetic(tkn_b)
        if not phonet_word_a or not phonet_word_b:
            return 0.0

        # Distancia de Levenshtein (operaciones necesarias para llegar a otra palabra) normalizada
        # De pato a gato la distancia es 1 ya que solo se necesita la sustitucion de 1 letra
        def levenshtein(word_a, word_b):
            if len(word_a) < len(word_b):
                return levenshtein(word_b, word_a)
            if len(word_b) == 0:
                return len(word_a)

            previous_row = list(range(len(word_b) + 1))
            for i, chars_a in enumerate(word_a):
                current_row = [i + 1]
                for j, chars_b in enumerate(word_b):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (chars_a != chars_b)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row

            distance = previous_row[-1]
            similarity = 1 - (distance / max(len(phonet_word_a), len(phonet_word_b)))
            return max(0, similarity) * 100

        return levenshtein(phonet_word_a, phonet_word_b)

    def semantic_similarity(self, tkn_a: str, tkn_b: str) -> float:
        # Calcula similitud semántica usando vectores de spaCy
        if not self.has_vectors:
            return 0.0

        doc1 = self.nlp(tkn_a)
        doc2 = self.nlp(tkn_b)
        if (
            doc1.has_vector
            and doc2.has_vector
            and doc1.vector_norm
            and doc2.vector_norm
        ):
            return doc1.similarity(doc2) * 100
        return 0.0

    def extract_analisis(self, analisis: List[Dict]) -> List[Dict]:
        # Se usan las palabras el analisis de la tokenización
        content_words = []
        for token in analisis:
            if not token.get("Stopword", True) and token.get("Gramatica") in [
                "NOUN",
                "ADJ",
                "VERB",
                "ADV",
            ]:
                content_words.append(
                    {
                        "palabra": token["Palabra"],
                        "lema": token["Lema"],
                        "posicion": token["Posicion"],
                        "gramatica": token["Gramatica"],
                    }
                )
        return content_words

    def synonyms(self, lema_a: str, lema_b: str) -> bool:
        # Verifica si dos palabras son sinónimos conocidos
        lm_a, lm_b = lema_a.lower(), lema_b.lower()
        return (
            lm_a in self.sinonimos_dict and lm_b in self.sinonimos_dict[lm_a]
        ) or (lm_b in self.sinonimos_dict and lm_a in self.sinonimos_dict[lm_b])

    def antonyms(self, lema_a: str, lema_b: str) -> bool:
        # Verifica si dos palabras son antónimos conocidos
        lm_a, lm_b = lema_a.lower(), lema_b.lower()
        return (
            lm_a in self.antonimos_dict and lm_b in self.antonimos_dict[lm_a]
        ) or (lm_b in self.antonimos_dict and lm_a in self.antonimos_dict[lm_b])

    def find_synon_anton(self, tokens_a: List[Dict], tokens_b: List[Dict]) -> Tuple[List, List]:
        # Pares de palabras para encontrar sinónimos y antónimos
        sinonimos = []
        antonimos = []
        # print("DEBUG - Analizando pares de palabras:")
        for token_a in tokens_a:
            for token_b in tokens_b:
                # print(token_a,token_b)
                if token_a["palabra"].lower() == token_b["palabra"].lower():
                    continue  # Ignorar palabras idénticas
                # Calcular similitud semántica
                sem_sim = self.semantic_similarity(token_a["lema"], token_b["lema"])
                # print(f"  {w1['palabra']} ({w1['gramatica']}) vs {w2['palabra']} ({w2['gramatica']}) = {sem_sim:.1f}%")
                # Sinónimos conocidos
                if self.synonyms(token_a["lema"], token_b["lema"]):
                    # print(f"Sinónimos conocido")
                    sinonimos.append(
                        {
                            "par": f"{token_a['palabra']} - {token_b['palabra']}",
                            "similitud": 100.0,  # Similitud máxima para sinónimos confirmados
                            "peso": 25,  # Peso alto para sinónimos confirmados
                        }
                    )
                # Antónimos conocidos
                elif self.antonyms(token_a["lema"], token_b["lema"]):
                    # print(f"Antónimo conocido")
                    antonimos.append(
                        {
                            "par": f"{token_a['palabra']} - {token_b['palabra']}",
                            "similitud": sem_sim,
                            "peso": 25,  # Peso alto para antónimos confirmados
                        }
                    )
                # Sinónimos por similitud semántica
                elif sem_sim >= self.umb_sinon * 100:
                    # Verificar que no sean antónimos conocidos
                    if not self.antonyms(token_a["lema"], token_b["lema"]):
                        print(f"Sinónimo por similitud ({sem_sim:.1f}% >= {self.umb_sinon*100}%)")
                        sinonimos.append(
                            {
                                "par": f"{token_a['palabra']}-{token_b['palabra']}",
                                "similitud": sem_sim,
                                "peso": 20,  # Peso alto para sinónimos
                            }
                        )
                # 4. Antónimos por baja similitud: solo para adjetivos
                elif (
                    token_a["gramatica"] == "ADJ"
                    and token_b["gramatica"] == "ADJ"
                    and self.umb_anton_min * 100
                    <= sem_sim
                    <= self.umb_anton_max * 100
                ):
                    if not self.antonyms(token_a["lema"], token_b["lema"]) and not self.synonyms(token_a["lema"], token_b["lema"]):
                        # print(f"Posible antónimo por baja similitud")
                        antonimos.append(
                            {
                                "par": f"{token_a['palabra']}-{token_b['palabra']}",
                                "similitud": sem_sim,
                                "peso": 10,  # Peso menor para antónimos inferidos
                            }
                        )

        # print(f"\nResultado: {len(sinonimos)} sinónimos, {len(antonimos)} antónimos")
        return sinonimos, antonimos

    """
    def calculate_phonetic_similarity(self, token_a: List[Dict], token_b: List[Dict]) -> float:
        # Calcula similitud fonética global entre dos conjuntos de palabras
        if not token_a or not token_b:
            return 0.0

        similarities = []
        for tkn_a in token_a:
            best_sim = 0
            for tkn_b in token_b:
                # Usar similitud semántica si está disponible, sino fonética básica
                if self.has_vectors:
                    sim = self.semantic_similarity(tkn_a["palabra"], tkn_b["palabra"])
                else:
                    sim = self.basic_phonetic_evaluation(tkn_a["palabra"], tkn_b["palabra"])
                best_sim = max(best_sim, sim)
            if best_sim > 0:
                similarities.append(best_sim)
        return round(np.mean(similarities) if similarities else 0.0, 1)
    """



    def calculate_phonetic_similarity(self, token_a: List[Dict], token_b: List[Dict]) -> float:
        def get_words(tokens):
            return [t.get("Palabra") or t.get("palabra", "") for t in tokens if t.get("Palabra") or t.get("palabra")]

        if not token_a or not token_b:
            return 0.0

        words_a = get_words(token_a)
        words_b = get_words(token_b)

        def best_matches(source, target):
            sims = []
            for w1 in source:
                best_score = 0.0
                for w2 in target:
                    if self.has_vectors:
                        score = self.semantic_similarity(w1, w2)
                    else:
                        score = self.basic_phonetic_evaluation(w1, w2)
                    best_score = max(best_score, score)
                sims.append(best_score)
            return sims

        sims_a_to_b = best_matches(words_a, words_b)
        sims_b_to_a = best_matches(words_b, words_a)

        all_scores = sims_a_to_b + sims_b_to_a
        return np.mean(all_scores) if all_scores else 0.0

    def evaluator(self, tokeni_a_data: Dict, tokeni_b_data: Dict) -> Dict:
        # Extraer palabras de contenido
        # print(tokeni_a_data["analisis"])
        # print(tokeni_b_data["analisis"])
        tokens_a = self.extract_analisis(tokeni_a_data["analisis"])
        tokens_b = self.extract_analisis(tokeni_b_data["analisis"])
        # Calcular similitud fonética/semántica global
        similitud_fonetica = self.calculate_phonetic_similarity(tokens_a, tokens_b)
        # Analizar relaciones semánticas
        if self.has_vectors:
            sinonyms_found, antonyms_found = self.find_synon_anton(tokens_a, tokens_b)
        else:
            sinonyms_found, antonyms_found = [], []

        # Preparar resultado final
        sinonimos = {
            "coincidencias": len(sinonyms_found),
            "palabras": [sinoms["par"] for sinoms in sinonyms_found],
            "peso": sum(sinoms["peso"] for sinoms in sinonyms_found),
        }
        antonimos = {
            "coincidencias": len(antonyms_found),
            "palabras": [antoms["par"] for antoms in antonyms_found],
            "peso": sum(antoms["peso"] for antoms in antonyms_found),
        }
        pond_similarity = round(
            (
                similitud_fonetica * 0.6
                + sinonimos["peso"] * 0.25
                + (100 - antonimos["peso"]) * 0.15
            ),
            2,
        )

        return {
            "simi_pond": pond_similarity,
            "similitud": similitud_fonetica,
            "sinonimos": sinonimos,
            "antonimos": antonimos,
        }


# Función wrapper para compatibilidad
# def evalue(data: Dict) -> Dict:
def evalue_phonetic(tokeni_a: Dict, tokeni_b: Dict) -> Dict:
    # data: 'tokeni_a' y 'tokeni_b'
    evaluator_instance = AdvancedPhoneticEvaluator()
    #return evaluator_instance.evaluator(data["tokeni_a"], data["tokeni_b"])
    return evaluator_instance.evaluator(tokeni_a, tokeni_b)

"""
if __name__ == "__main__":
    # Datos de ejemplo (tokeni_a y tokeni_b tambien devuelven un "resumen" pero no es necesario para la evaluacion fonetica)
    ejemplo_data = {
        "tokeni_a": {
            "origin": "la buena cahorra surenia de los 38 cacahuates",
            "analisis": [
                {"Posicion": 1,"Stopword": False,"Palabra": "buena","Lema": "bueno","Gramatica": "ADJ",},
                {"Posicion": 2,"Stopword": False,"Palabra": "cahorra","Lema": "cahorra","Gramatica": "NOUN",},
                {"Posicion": 3,"Stopword": False,"Palabra": "surenia","Lema": "surenia","Gramatica": "PROPN",},
                {"Posicion": 7,"Stopword": False,"Palabra": "cacahuates","Lema": "cacahuate","Gramatica": "NOUN",},
            ],
        },
        "tokeni_b": {
            "origin": "el perrito malo surenio de los 38 cacahuates",
            "analisis": [
                {"Posicion": 1,"Stopword": False,"Palabra": "perrito","Lema": "perrito","Gramatica": "NOUN",},
                {"Posicion": 2,"Stopword": False,"Palabra": "malo","Lema": "malo","Gramatica": "ADJ",},
                {"Posicion": 3,"Stopword": False,"Palabra": "surenio","Lema": "surenio","Gramatica": "NOUN",},
                {"Posicion": 7,"Stopword": False,"Palabra": "cacahuates","Lema": "cacahuate","Gramatica": "NOUN",},
            ],
        },
    }

    try:
        resultado = evalue_phonetic(ejemplo_data["tokeni_a"], ejemplo_data["tokeni_b"])
        print("Resultado:")
    except Exception as e:
        print(f"Error: {e}")
        print("\nPara instalar dependencias:")
        print("pip install spacy")
        print("python -m spacy download es_core_news_md")
"""
