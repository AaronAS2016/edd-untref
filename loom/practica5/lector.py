import os
import re
from utils import remover_digitos, remover_caracteres, remover_caracteres_especiales, es_numero_romano
from excepciones import NoEncontroArchivoIndice


class LectorIndice:
    _remover_pag_regex = r'\((p|P)([0-9]){1,}\)'
    _remover_marca_glosario = r"\[([0-9])*\-([0-9])*]"

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
            raise NoEncontroArchivoIndice(self.__archivo)

    def __buscar_indice(self, lector, texto):
        '''
        Busco el indice y guardo el numero de linea donde se encuentra para luego procesarlo
        '''
        linea_indice = -1
        for linea, valor in enumerate(texto):
            if valor.find("CONTENTS") != -1:
                linea_indice = linea
                return linea_indice
        return linea_indice

    def __procesar_indice(self, lector, texto):
        '''
        Desde la posicion  del indice voy buscando las novelas y guardo el numero de pagina donde arranca cada una 
        para luego poder recortar los textos
        '''
        listado_de_paginas = []
        for valor in texto:
            sanitaze_valor = remover_digitos(valor)
            if sanitaze_valor in self.__novelas:
                listado_de_paginas.append(remover_caracteres(valor))

            if len(listado_de_paginas) == len(self.__novelas):
                break
        return listado_de_paginas

    def __agregar_linea_a_novela(self, novela, linea_a_guardar):
        self.__textos_novelas[novela].append(linea_a_guardar)

    def __recortar_textos(self, lector, texto, listado_de_paginas):
        '''
        Recorto los textos filtrandolos por el numero de pagina que procese del indice
        '''
        textos_encontrados = 0
        lineas_procesadas = 0
        guardar_texto = False
        texto_actual = -1
        es_ultimo_cuento = False
        while(textos_encontrados <= len(self.__novelas) or es_ultimo_cuento):

            linea_actual = texto[lineas_procesadas]

            es_ultimo_cuento = textos_encontrados == len(self.__novelas)

            if es_ultimo_cuento and self.__encontro_epilogo(linea_actual):
                # En caso de encontrar el epilogo se deja de guardar
                es_ultimo_cuento = False
                guardar_texto = False
                textos_encontrados += 1

            se_encontro_todos_los_textos = textos_encontrados >= len(
                self.__novelas)

            #Si no es el ultimo cuento o se encontro todas las novelas, no avanzo al siguiente
            if not es_ultimo_cuento and not se_encontro_todos_los_textos and self.__encontro_numero_de_pagina(linea_actual, listado_de_paginas[textos_encontrados]):
                texto_actual += 1
                textos_encontrados += 1
                guardar_texto = True
            
            #En caso que se haya encontrado alguna novela, se empieza a guardar las linea en el diccionario
            if guardar_texto:
                linea_a_guardar = self.__sanatizar_linea(linea_actual)
                # Si no es el titulo de la novela o un numero romando que indica el inicio de los capitulos, lo guardo
                if not self.__es_titulo_de_novela(linea_a_guardar, texto_actual) and not es_numero_romano(linea_a_guardar):
                    self.__agregar_linea_a_novela(novela=self.__novelas[texto_actual], linea_a_guardar=linea_a_guardar)
    
            lineas_procesadas += 1

    def __es_titulo_de_novela(self, novela, novela_actual):
        return novela == self.__novelas[novela_actual]

    def __encontro_numero_de_pagina(self, linea, pagina):
        return linea.find(f"(p{pagina})") != -1

    def __encontro_epilogo(self, linea):
        return self.__sanatizar_linea(linea).find("EPÍLOGO") != -1

    def __eliminar_marca_glosario(self, linea):
        return re.sub(self._remover_marca_glosario, "", linea)

    def __eliminar_numero_de_linea(self, linea):
        linea_sanatizada = linea
        if linea[:2].isdigit():
            linea_sanatizada = linea[3:]
        return linea_sanatizada

    def __eliminar_guiones_de_dialogo(self, linea):
        return linea.replace("--", " ")

    def __eliminar_numero_de_pag(self, linea):
        return re.sub(self._remover_pag_regex, '', linea)

    def __sanatizar_linea(self, linea):
        linea_sanatizada = self.__eliminar_numero_de_pag(linea)
        linea_sanatizada = self.__eliminar_marca_glosario(linea_sanatizada)
        linea_sanatizada = self.__eliminar_guiones_de_dialogo(linea_sanatizada)
        linea_sanatizada = self.__eliminar_numero_de_linea(
            linea_sanatizada)
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
