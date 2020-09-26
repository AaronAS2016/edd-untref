class Cliente:
    def __init__(self, nombre_completo=None, dni=None):
        if nombre_completo is not None and dni is not None:
            self.__nombre_completo = nombre_completo
            self.__dni = dni
        else:
            self.__nombre_completo = 'Usuario anonimo'
            self.__dni = 'Dni anonimo'

    def enviar_mensaje(self, mensaje):
        # Envia el mensaje...
        pass

    def get_nombre(self):
        return self.__nombre_completo

    def get_dni(self):
        return self.__dni

    def __str__(self):
        return f"{{'nombre': '{self.__nombre_completo}','dni': '{self.__dni}' }}"


class Cuenta:

    def __init__(self, saldo=None, cliente=None):
        if saldo is not None and cliente is not None:
            self.__saldo = saldo
            self.__numero = cliente

    def depositar(self, importe):
        # Deposita ...
        pass

    def extraer(self, importe_a_extraer):
        # Extrae...
        pass


class CuentaSueldo(Cuenta):

    def __init__(self, empleador, cuit_empleador, extracciones_permitidas, extracciones_realizadas):
        self.__empleador = empleador
        self.__cuit_empleador = cuit_empleador
        self.__extracciones_permitidas = extracciones_permitidas
        self.__extracciones_realizadas = extracciones_realizadas

    def _incrementar_extracciones_realizadas(self):
        # Incrementa maximo...
        pass

    def reset_extracciones_realizadas(self):
        # Reset...
        pass

    def extraer(self, importe):
        # Extrae...
        pass


class Descubierto:

    def get_descubierto(self):
        pass

    def obtener_disponible(self):
        pass

    def aviso_descubierto(self):
        pass

    def set_descubierto(self):
        pass


class CuentaMultipersona(Cuenta, Descubierto):

    __cotitulares = []

    def __init__(self, cliente=None):
        if cliente is not None:
            self.__cotitulares.append(cliente)

    def agregar_cotitular(self, cliente):
        # Agrega cotitular...
        pass

    def get_descubierto(self):
        # Retorna descubierto
        return 0

    def obtener_disponible(self):
        # Retorna disponible...
        return 0

    def aviso_descubierto(self):
        # realiza el aviso...
        pass

    def set_descubierto(self):
        # define descubierto
        pass


class CuentaSueldoPlus(CuentaSueldo, Descubierto):

    def __init__(self, cliente, descubierto, disponible):
        self.__cliente = cliente
        self.__descubierto = descubierto
        self.__disponible = disponible

    def set_cantidad_extracciones(self, extracciones):
        # setea extracciones
        pass

    def obtener_disponible(self):
        # obteniendo disponible
        return 0

    def aviso_descubierto(self):
        # realiza el aviso...
        pass

    def set_descubierto(self):
        # define descubierto
        pass

    def get_descubierto(self):
        # obtiene descubierto
        return 0
