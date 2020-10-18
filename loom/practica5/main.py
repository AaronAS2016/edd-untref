from lector import LectorIndice 
from indice import IndiceInvertidoBTree
from pprint import pprint as pp



class IndiceNovelas:
    def __init__(self, archivo, novelas):
        self.__procesar_archivos(archivo, novelas)
        self.__indice_invertido = IndiceInvertidoBTree(novelas)

    def __procesar_archivos(self, archivo, novelas):
        LectorIndice(archivo, novelas)

    def obtener_indice(self):
        return self.__indice_invertido.obtener_indice()

    def buscar(self, palabra):
        return self.__indice_invertido.buscar(palabra)



if __name__ == "__main__":
    novelas = [
        "LA BUENAVENTURA",
        "LA CORNETA DE LLAVES",
        "LAS DOS GLORIAS",
        "EL AFRANCESADO",
        "¡VIVA EL PAPA!",
        "EL EXTRANJERO",
        "EL LIBRO TALONARIO",
        "MOROS Y CRISTIANOS",
        "EL AÑO EN SPITZBERG"
    ]
    archivo = "novelas.txt"

    indice = IndiceNovelas(archivo, novelas)
    pp(list(indice.obtener_indice().items()))
        