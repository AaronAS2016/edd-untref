class NoSeEncontroPalabra(Exception):
    def __init__(self, palabra):
        message = f"La palabra: {palabra} no se encontro en el indice"
        super().__init__(message)


class NoEncontroArchivoIndice(Exception):
    def __init__(self, archivo):
        message = f"No se encontro el archivo {archivo} en disco, compruebe que exista y vuelva a intentarlo"
        super().__init__(message)
