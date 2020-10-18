from lector import LectorIndice 
from indice import IndiceInvertido
from pprint import pprint as pp
from excepciones import NoSeEncontroPalabra



class IndiceNovelas:
    def __init__(self, archivo, novelas):
        self.__procesar_archivos(archivo, novelas)
        self.__indice_invertido = IndiceInvertido(novelas)

    def __procesar_archivos(self, archivo, novelas):
        LectorIndice(archivo, novelas)

    def obtener_indice(self):
        return self.__indice_invertido.obtener_indice()

    def buscar(self, palabra):
        resultado = self.__indice_invertido.buscar(f"{palabra}*")
        if len(resultado[0]) == 0:
            raise NoSeEncontroPalabra(palabra)
        
        return resultado



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

    palabras_a_buscar = [
        'vicario',
        'forastero',
        'parapeto',
        'tremebundo',
        'guillotina',
        'apellido',
        'caos',
        'entuerto',
        'suplicante',
        'continente'
    ]

    archivo = "novelas.txt"

    indice = IndiceNovelas(archivo, novelas)
    
    for palabra in palabras_a_buscar:
        try:
            pp(indice.buscar(palabra))
        except NoSeEncontroPalabra as error:
            pp(str(error))
