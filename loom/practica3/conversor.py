from clases import Cliente

def convertir_dicc_a_instancia(dicc):
    return Cliente(dicc["nombre"],dicc["dni"]) if bool(dicc) else []
    


def convertir_instancia_a_dicc(instancia):
    return { "nombre": instancia.get_nombre(), "dni": instancia.get_dni() }
