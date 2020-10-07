import os
import csv
import struct


class Lector:

    def __init__(self, archivo):
        if os.path.getsize(archivo):
            self.__archivo = archivo

    def leer_datos_csv(self, iterador, archivo=None, informacion_recibida={}):
        if archivo is None:
            archivo = self.__archivo

        with open(archivo, 'r') as csvReader:
            lector = csv.DictReader(csvReader)
            for informacion in lector:
                informacion_recibida = iterador(
                    informacion_recibida, informacion)

        return informacion_recibida

class Escritor:

    def __init__(self, configuracion):

        self.__configuracion = configuracion

    def __calcular_longitud_campos(self, campos):

        formato = ''.join(f"{campo[1]}s" for campo in campos)

        return formato

    def guardar_contacto(self, iterador_escritura, datos, archivo, campos=None):

        formato = self.__calcular_longitud_campos(
            campos) if campos is not None else ""

        with open(self.__configuracion[archivo], "ab") as escritor:
            iterador_escritura(escritor, datos, formato)


class EscritorCovid(Escritor):

    def __init__(self, informacion, ubicacion_de_salida):
        self.__informacion = informacion
        super().__init__(ubicacion_de_salida)

    def guardar_todo(self):
        self.guardar_informacion_casos_mayores_casos_por_provincia()
        self.guardar_informacion_rango_etario()
        self.guardar_informacion_casos_provincia()
        self.guardar_informacion_promedio_edad()

    def guardar_informacion_rango_etario(self):
        campos = [("0-20", 10), ("20-40", 10), ("20-60", 10),
                  ("60+", 10), ("Sin informacion", 10)]

        self.guardar_contacto(
            self.__iterador_guardado_rango_etario, self.__informacion["cantidad_casos_por_rango_etario"], "rango_etario", campos)

    def guardar_informacion_casos_provincia(self):
        campos = [("Mujeres", 10),
                  ("Hombres", 10), ("No Reconocido", 10)]

        self.guardar_contacto(
            self.__iterador_guardado_casos_provincias, self.__informacion["cantidad_casos_por_provincia"], "provincia", campos)

    def guardar_informacion_casos_mayores_casos_por_provincia(self):

        self.guardar_contacto(
            self.__iterador_guardado_por_mayores_casos, self.__informacion["provincias_con_mayor_casos"], "mayor_cantidad_de_casos")

    def guardar_informacion_promedio_edad(self):

        self.guardar_contacto(
            self.__iterador_guardado_promedio_edad, self.__informacion["promedio_edad_infectado"], "edad_promedio")

    @staticmethod
    def __iterador_guardado_casos_provincias(escritor, datos, formato):
        for casos in datos.values():
            casos_hombres = str(casos["M"]).encode()
            casos_mujeres = str(casos["F"]).encode()
            casos_no_reconocido = str(casos["NR"]).encode()
            escritor.write(struct.pack(formato, casos_mujeres, casos_hombres, casos_no_reconocido))

    @staticmethod
    def __iterador_guardado_rango_etario(escritor, datos, formato):

        casos_entre_cero_y_veinte = str(datos["0-20"]).encode()
        casos_entre_veinte_y_cuarenta = str(datos["20-40"]).encode()
        casos_entre_cuarenta_y_sesenta = str(datos["40-60"]).encode()
        casos_mas_de_60 = str(datos["60+"]).encode()
        casos_sin_informacion = str(datos["Sin informacion"]).encode()
        escritor.write(struct.pack(formato, casos_entre_cero_y_veinte, casos_entre_veinte_y_cuarenta,
                                   casos_entre_cuarenta_y_sesenta, casos_mas_de_60, casos_sin_informacion))

    @staticmethod
    def __iterador_guardado_promedio_edad(escritor, datos, formato):

        for informacion in datos.values():
            promedio = informacion['promedio']
            longitud = len(str(promedio))
            escritor.write(
                f"{longitud},{promedio}-".encode())

    @staticmethod
    def __iterador_guardado_por_mayores_casos(escritor, datos, formato):
        for _, casos in datos:

            longitud_casos = len(f"{casos}")

            escritor.write(
                f"{longitud_casos},{casos}-".encode())
