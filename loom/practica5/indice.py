from nltk.stem import SnowballStemmer  # Stemmer
from nltk.corpus import stopwords  # Stopwords
from BTrees.OOBTree import OOBTree
import string


class IndiceInvertidoBTree:

    def __init__(self, documentos):
        self.stop_words = frozenset(
            stopwords.words('spanish'))  # lista de stop words
        self._docs = self.__leer_documentos(documentos)
        self._spanish_stemmer = SnowballStemmer(
            'spanish', ignore_stopwords=False)
        self.__docs_to_docID()
        self.__generar_indice()

    def __leer_documentos(self, documentos):
        docs = {}
        for documento in documentos:
            with open(f"{documento}.txt", "r") as lector:
                docs[documento] = ''.join(lector.readlines())
        return docs

    def __docs_to_docID(self):
        self._doc_to_docID = {}
        docID = 0
        for doc in self._docs.keys():
            self._doc_to_docID[doc] = docID
            docID += 1
        self._docID_to_doc = dict((v, k)
                                  for k, v in self._doc_to_docID.items())

    def __lematizar_palabra(self, palabra):
        reemplazos = (("á", "a"), ("é", "e"),
                      ("ó", "o"), ("ú", "u"), ("í", "i"))
        palabra = palabra.lower()
        palabra = palabra.strip(string.punctuation+"»"+"\x97"+"¿"+"¡" + "?" + "!")
        for a, b in reemplazos:
            palabra = palabra.replace(a, b)
        palabra_lematizada = palabra
        return palabra_lematizada

    def __generar_indice(self):
        ''' Genera los pares la lista de pares (palabra, docID) ordenada por palabra
        '''
        pares = []
        indice = OOBTree()

        for doc in self._docs:
            lista_palabras = [palabra for palabra in self._docs[doc].split(
            ) if not palabra in self.stop_words]
            lista_palabras = [self.__lematizar_palabra(
                palabra) for palabra in lista_palabras]

            pares = pares + [(palabra, self._doc_to_docID[doc])
                             for palabra in lista_palabras]
        for par in pares:
            posting = indice.setdefault(par[0], set())
            posting.add(par[1])
        self._indice = indice

    def __buscar(self, palabra):
        alfabeto = 'abcdefghijklmnñopqrstuvwxyz'

        ultimo = palabra[-1]
        palabra_final = palabra[:-1] + \
            alfabeto[(alfabeto.find(ultimo)+1) % len(alfabeto)]
        palabras = set()
        claves = list(self._indice.keys())
        menor = claves.index(self._indice.minKey(palabra))
        mayor = claves.index(self._indice.minKey(palabra_final))
        palabras = set(claves[menor:mayor])

        return palabras

    def buscar(self, palabra):
        palabras = set()
        resultados = set()
        palabra_lematizada = self.__lematizar_palabra(palabra)

        if palabra.find("*") == -1:
            if palabra_lematizada in self._indice:
                palabras.add(palabra_lematizada)
        elif palabra[-1] == "*":
            palabras = self.__buscar(palabra[:-1])

        for pal in palabras:
            for docID in self._indice[pal]:
                resultados = resultados | {self._docID_to_doc[docID]}

        return palabras, resultados

    def obtener_indice(self):
        return self._indice