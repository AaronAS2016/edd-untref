import pathlib
import os
import csv
import struct
from escritor import Lector, EscritorCovid

# Configuracion
ubicacion_archivo = f"{pathlib.Path(__file__).parent.absolute()}/test.csv"


class EstadisticaCovid:

    __configuracion = {
        "paths": {
            "provincia" : f"{pathlib.Path(__file__).parent.absolute()}/casos_provincia",
            "edad_promedio" : f"{pathlib.Path(__file__).parent.absolute()}/edad",
            "mayor_cantidad_de_casos" : f"{pathlib.Path(__file__).parent.absolute()}/mayores_casos",
            "rango_etario" : f"{pathlib.Path(__file__).parent.absolute()}/rango_etario"
        }
    } 

    def __init__(self, archivo, config=None):
        if config is not None:
            self.__configuracion = config 
        self.__lector = Lector(archivo)
        self.__informacion_guardada = {'cantidad_casos_por_provincia': {
        }, "cantidad_casos_por_rango_etario": {"0-20": 0, "20-40": 0, "40-60": 0, "60+": 0, "Sin informacion": 0},
            'promedio_edad_infectado': {},
            'provincias_con_mayor_casos': {}
        }

    def comenzar_analisis(self):
        informacion_recibida = self.__lector.leer_datos_csv(
            self.iterador_estadistica_covid, informacion_recibida=self.__informacion_guardada)

        mayores_casos_ordenados = sorted(
            informacion_recibida['provincias_con_mayor_casos'].items(), key=lambda provincia_casos: provincia_casos[1], reverse=True)
        informacion_recibida['provincias_con_mayor_casos'] = mayores_casos_ordenados

        self.__informacion_guardada = informacion_recibida

    def guardar_analisis(self):
        escritor = EscritorCovid(self.__informacion_guardada, self.__configuracion["paths"]) 
        escritor.guardar_todo()

    @staticmethod
    def procesar_edad(edad, anio_meses):
        if not edad:
            return "Sin informacion"

        rango_edad = ''

        if int(edad) >= 0 and int(edad) < 20 or anio_meses == "Meses":
            rango_edad = "0-20"
        elif int(edad) >= 20 and int(edad) < 40:
            rango_edad = "20-40"
        elif int(edad) >= 40 and int(edad) < 60:
            rango_edad = "40-60"
        elif int(edad) >= 60:
            rango_edad = "60+"
        return rango_edad

    @staticmethod
    def procesar_promedio(edad, edad_promedio, anio_meses):
        if not edad:
            return edad_promedio

        edad_contable =  12 / edad if anio_meses == "Meses" else edad
        cantidad =  edad_promedio['cantidad']
        promedio = edad_promedio['promedio']

        nueva_cantidad = cantidad + 1
        nuevo_promedio = promedio + ((int(edad_contable) - promedio) / nueva_cantidad)

        return {"promedio": nuevo_promedio, 'cantidad': nueva_cantidad}

    @staticmethod
    def iterador_estadistica_covid(informacion_almacenada, informacion_recibida):
        # 1. Cantidad de casos por provincia, separados por género
        sexo = informacion_recibida["sexo"]

        provincia = informacion_recibida["residencia_provincia_nombre"]
        informacion_almacenada['cantidad_casos_por_provincia'].setdefault(
            provincia, {"M": 0, "F": 0, "NR": 0})

        informacion_almacenada['cantidad_casos_por_provincia'][provincia][sexo] += 1
        # 2. Cantidad de casos por rango etario (0 a 20, 20 a 40, 40 a 60, 60 o más)
        edad = informacion_recibida["edad"]
        anio_meses = informacion_recibida['edad_años_meses']
        rango_edad = EstadisticaCovid.procesar_edad(edad, anio_meses)

        informacion_almacenada['cantidad_casos_por_rango_etario'][rango_edad] += 1

        # 3 Promedio de edad de los infectados por provincia
        informacion_almacenada['promedio_edad_infectado'].setdefault(provincia, { "promedio": 0, "cantidad":0 })
        informacion_almacenada['promedio_edad_infectado'][provincia] = EstadisticaCovid.procesar_promedio(
            edad, informacion_almacenada['promedio_edad_infectado'][provincia], anio_meses)

        # 4. Provincias ordenadas por cantidad de casos, con los casos

        informacion_almacenada['provincias_con_mayor_casos'].setdefault(
            provincia, 0)
        informacion_almacenada['provincias_con_mayor_casos'][provincia] += 1

        return informacion_almacenada

    def obtener_resultados(self):
        return self.__informacion_guardada


if __name__ == "__main__":

    estadistica = EstadisticaCovid(ubicacion_archivo)
    estadistica.comenzar_analisis()
    estadistica.guardar_analisis()

    resultados = estadistica.obtener_resultados()
    print(resultados["promedio_edad_infectado"])
