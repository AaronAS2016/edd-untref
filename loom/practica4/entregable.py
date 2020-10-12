import pathlib
import os
import csv
import struct
import struct
from pprint import pprint as pp

# Configuracion
ubicacion_archivo = f"{pathlib.Path(__file__).parent.absolute()}/Covid19Casos.csv"


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
            escritor.write(struct.pack(formato, casos_mujeres,
                                       casos_hombres, casos_no_reconocido))

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

        for provincia, informacion in datos.items():
            longitud_provincia = len(provincia)
            promedio = informacion['promedio']
            longitud = len(str(promedio))
            escritor.write(
                f"{longitud_provincia},{provincia},{longitud},{promedio}-".encode())

    @staticmethod
    def __iterador_guardado_por_mayores_casos(escritor, datos, formato):
        for provincia, casos in datos:

            longitud_provincia = len(provincia)
            longitud_casos = len(str(casos))

            escritor.write(
                f"{longitud_provincia},{provincia},{longitud_casos},{casos}-".encode())


class EstadisticaCovid:

    __configuracion = {
        "paths": {
            "provincia": f"{pathlib.Path(__file__).parent.absolute()}/casos_provincia",
            "edad_promedio": f"{pathlib.Path(__file__).parent.absolute()}/edad",
            "mayor_cantidad_de_casos": f"{pathlib.Path(__file__).parent.absolute()}/mayores_casos",
            "rango_etario": f"{pathlib.Path(__file__).parent.absolute()}/rango_etario"
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
        escritor = EscritorCovid(
            self.__informacion_guardada, self.__configuracion["paths"])
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

        edad_contable = 0 if anio_meses == "Meses" else edad
        cantidad = edad_promedio['cantidad']
        promedio = edad_promedio['promedio']

        nueva_cantidad = cantidad + 1
        nuevo_promedio = promedio + \
            ((int(edad_contable) - promedio) / nueva_cantidad)

        return {"promedio": nuevo_promedio, 'cantidad': nueva_cantidad}

    @staticmethod
    def iterador_estadistica_covid(informacion_almacenada, informacion_recibida):

        if informacion_recibida["clasificacion_resumen"] == "Confirmado":
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
            informacion_almacenada['promedio_edad_infectado'].setdefault(
                provincia, {"promedio": 0, "cantidad": 0})
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
    pp(resultados)
