import os
from utils import remover_digitos, remover_caracteres, remover_caracteres_especiales, es_numero_romano

class NoEncontroArchivoIndice(Exception):
    pass


class LectorIndice:
    def __init__(self, archivo, novelas):
        self.__archivo = archivo
        self.__novelas = novelas
        self.__textos_novelas = {novela: [] for novela in novelas}
        self.__procesar_archivo()
        self.__guardar_archivos()

    def __guardar_archivos(self):
        escritor = EscritorIndice()
        for titulo, texto in self.__textos_novelas.items():
            escritor.escribir_archivo(titulo, texto)

    def __procesar_archivo(self):
        try:
            with open(self.__archivo, "r") as lector:
                texto = lector.readlines()
                texto = texto[self.__buscar_indice(lector, texto):]
                listado_de_paginas = self.__procesar_indice(lector, texto)
                self.__recortar_textos(lector, texto, listado_de_paginas)
        except FileNotFoundError:
            raise NoEncontroArchivoIndice

    def __buscar_indice(self, lector, texto):
        linea_indice = -1
        for linea, valor in enumerate(texto):
            if valor.find("CONTENTS") != -1:
                linea_indice = linea
                return linea_indice
        return linea_indice

    def __procesar_indice(self, lector, texto):
        listado_de_paginas = []
        for valor in texto:
            sanitaze_valor = remover_digitos(valor)
            if sanitaze_valor in self.__novelas:
                listado_de_paginas.append(remover_caracteres(valor))

            if len(listado_de_paginas) == len(self.__novelas):
                break
        return listado_de_paginas

    def __recortar_textos(self, lector, texto, listado_de_paginas):
        textos_encontrados = 0
        lineas_procesadas = 0
        guardar_texto = False
        texto_actual = -1
        es_ultimo_cuento = False
        while(textos_encontrados < len(self.__novelas) or es_ultimo_cuento):

            linea_actual = texto[lineas_procesadas]

            if not es_ultimo_cuento and self.__encontro_numero_de_pagina(linea_actual, listado_de_paginas[textos_encontrados]):
                texto_actual += 1
                textos_encontrados += 1
                guardar_texto = True

            if guardar_texto:
                linea_a_guardar = self.__sanatizar_linea(linea_actual)
                if not self.__es_titulo_de_novela(linea_a_guardar, texto_actual) and not es_numero_romano(linea_a_guardar):
                    self.__textos_novelas[self.__novelas[texto_actual]].append(
                        linea_a_guardar)

            es_ultimo_cuento = textos_encontrados == len(self.__novelas)

            if self.__encontro_epilogo(linea_actual):
                es_ultimo_cuento = False
                guardar_texto = False

            lineas_procesadas += 1

    def __es_titulo_de_novela(self, novela, novela_actual):
        return novela == self.__novelas[novela_actual]

    def __encontro_numero_de_pagina(self, linea, pagina):
        return linea.find(f"(p{pagina})") != -1

    def __encontro_epilogo(self, linea):
        return self.__sanatizar_linea(linea).find("EPÍLOGO") != -1

    def __sanatizar_linea(self, linea):
        linea_sanatizada = remover_digitos(linea)
        linea_sanatizada = linea_sanatizada.replace("(p)", "")
        linea_sanatizada = remover_caracteres_especiales(linea_sanatizada)
        linea_sanatizada = linea_sanatizada.strip()
        return linea_sanatizada


class EscritorIndice:

    def escribir_archivo(self, nombre_archivo, contenido):
        if os.path.exists(nombre_archivo):
            os.remove(nombre_archivo)

        with open(f"{nombre_archivo}.txt", "w") as escritor:
            for linea in contenido:
                escritor.write(linea)
                escritor.write("\n")

