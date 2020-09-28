from config import localizacion
from excepciones import NoHayUsuarioCreadoError
from conversor import convertir_dicc_a_instancia, convertir_instancia_a_dicc
import pickle
import json
import shelve
import os


def chequear_data_guardada(f):
    def chequear_data_guardada_decorator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (json.decoder.JSONDecodeError, EOFError):
            raise NoHayUsuarioCreadoError("No hay un cliente guardado")
            
    return chequear_data_guardada_decorator


def guardar_informacion(data, method="pickle"):

    if method == 'pickle':
        guardar_informacion_pickle(data)
    elif method == "shelve":
        guardar_informacion_shelve(data)
    else:
        guardar_informacion_json(data)


def guardar_informacion_pickle(data, ubicacion=localizacion["pickle"]):
    with open(ubicacion, "wb") as escritor:
        pickle.dump(data, escritor)


def guardar_informacion_json(data, ubicacion=localizacion["json"], parsear_data=convertir_instancia_a_dicc):
    with open(ubicacion, "w") as escritor:
        json.dump(convertir_instancia_a_dicc(data), escritor)

def guardar_informacion_shelve(data,  ubicacion=localizacion["shelve"]):
    with shelve.open(ubicacion) as escritor:
        escritor["persona"] = data


def recuperar_informacion(method="pickle"):
    se_pudo_recuperar = False

    if method == 'pickle':
        se_pudo_recuperar = recuperar_informacion_pickle()
    elif method == "shelve":
        se_pudo_recuperar = recuperar_informacion_shelve()
    else:
        se_pudo_recuperar = recuperar_informacion_json()

    return se_pudo_recuperar

@chequear_data_guardada
def recuperar_informacion_pickle(ubicacion=localizacion["pickle"]):
    data_recuperada = []
    with open(ubicacion, "rb") as lector:
        data_recuperada = pickle.load(lector)
    return data_recuperada

@chequear_data_guardada
def recuperar_informacion_json(ubicacion=localizacion["json"], parsear_data=convertir_dicc_a_instancia):
    data_recuperada = []
    with open(ubicacion, "r") as lector:
        data_recuperada = parsear_data(json.load(lector))
    return data_recuperada


@chequear_data_guardada
def recuperar_informacion_shelve(ubicacion=localizacion["shelve"]):
    data_recuperada = []
    with shelve.open(ubicacion) as lector:
        if "persona" in lector:
            data_recuperada = lector["persona"]
    return data_recuperada


