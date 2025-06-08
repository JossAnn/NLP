# NLP

Natural Language Processing

### Limpieza de entradas de texto

Archivo cleaner.py

* Convierte a minúsculas
* Elimina tildes y caracteres no ASCII
* Elimina signos de puntuación
* Elimina caracteres no alfanuméricos (excepto espacios)
* Quita espacios múltiples
* Devuelve un texto plano en minusculas sin caracteres no alfanumericos, puntuación o espacios multiples

### Transliteración

Archivo transliterator.py

* Intercambia numeros dentro de las palabras por letras
* Mantiene cantidades dentro de una oración
* Empareja texto original con su transliteración
* Devuelve:
  * Texto original [origin_text] (str)
  * Texto transliterado [text_trans] (str)
  * Numero de transliteraciones que se hicieron [num_trans] (int)
  * Lista de las palabras transliteradas [words_trans] (list[tuple[str,str]])

### Tokenización

Archivo tokenizer.py

* Usa el modelo es_core_news_sm. Es necesario: `pip install spacy` y luego: `python -m spacy download es_core_news_sm`
* Analiza cada token (palabra) del texto de entrada y obtiene las propiedades:
  * Posicion (int) => Es la posicion del token dentro del texto
  * Stopword (bool) => Es una palabra común (el, de, los) que aporta poco significado semántico.
  * Palabra (str) => Es la palabra que ha sido recibida
  * Lema (str) => Es la forma base de una palabra
  * Gramatica (str) => Devuelve si es un sustantivo, verbo, adjetivo, etc.
  * Genero
  * Numero
* hace un resumen del texto de entrada y lo clasifica en cuatro categorías:
  * Singulares
  * Plurales
  * Masculino
  * Femenino
* Devuelve ambbas salidas tanto del analisis como del resumen
