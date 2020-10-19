

from pprint import pprint as pp
from excepciones import NoSeEncontroPalabra
from indice import IndiceNovelas

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
