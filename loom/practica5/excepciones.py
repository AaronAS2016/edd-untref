class NoSeEncontroPalabra(Exception):
    def __init__(self, palabra):
        message = f"La palabra: {palabra} no se encontro en el indice"
        super().__init__(message)

class NoEncontroArchivoIndice(Exception):
    pass