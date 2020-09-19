import random

class Evento():

    def __init__(self, nombre, hora):
        self._nombre = nombre
        self._hora = self.__validar_hora(hora)
        self._asistentes_inscriptos = []

    def __validar_hora(self, hora):
        inicio, fin = hora
        if fin < inicio:
            raise TypeError("El horario de horario de inicio no puede ser menor al final")
        return hora
    
    def obtener_hora(self):
        return self._hora
    
    def obtener_nombre(self):
        return self._nombre
    
    def obtener_inscriptos(self):
        return self._asistentes_inscriptos
    
    def cruzan_horarios(self, horario_a, horario_b):
       inicio_a, final_a = horario_a
       inicio_b, final_b = horario_b
       return inicio_a <= final_b and final_a >= inicio_b

    def se_puede_anotar(self, eventos):
        se_puede_anotar = True
        for evento in eventos:
            cruzan_horarios_con_algun_evento = self.cruzan_horarios(self.obtener_hora(), evento.obtener_hora()) 
            if cruzan_horarios_con_algun_evento:
               se_puede_anotar = False
        return se_puede_anotar

    def inscribir(self, nombre, asistente):
        asistente.anotar_a_evento(self)
        self._asistentes_inscriptos.append(nombre)
  
    def anotar_asistente(self, asistente):
        nombre = asistente.obtener_nombre()
        eventos_a_asistir = asistente.obtener_eventos()
        se_puede_anotar = self.se_puede_anotar(eventos_a_asistir)

        if se_puede_anotar:
            self.inscribir(nombre, asistente)
        return se_puede_anotar

    def __repr__(self):
        return self._nombre

class Evento_exclusivo(Evento):

    def __init__(self, nombre, hora, cupo):
        Evento.__init__(self, nombre, hora)
        self.__cupo = cupo
    
    def obtener_cupo(self):
        return self.__cupo
    
    def se_puede_anotar(self, eventos):
        return Evento.se_puede_anotar(self, eventos) and self.__cupo > 0
    
    def inscribir(self, nombre, asistente):
        Evento.inscribir(self, nombre, asistente)
        self.__cupo-=1

    def obtener_inscriptos(self):
        return self._asistentes_inscriptos

    def anotar_asistente(self, asistente):
        nombre = asistente.obtener_nombre()
        eventos_a_asistir = asistente.obtener_eventos()
        se_puede_anotar = self.se_puede_anotar(eventos_a_asistir)

        if se_puede_anotar:
            self.inscribir(nombre, asistente)
        
        return se_puede_anotar

class Asistente():

    def __init__(self, nombre):
        self.__nombre = nombre
        self.__eventos = []

    def obtener_eventos(self):
        return self.__eventos
    
    def obtener_nombre(self):
        return self.__nombre

    def anotar_a_evento(self, evento):
        self.__eventos.append(evento)
    
    def __repr__(self):
        return self.__nombre
        
def mezclar(lista):
    return random.sample(lista, len(lista))

def organizar_asistentes(lista_de_asistentes):
    return [Asistente(nombre_asistente) for nombre_asistente in lista_de_asistentes]

def asistentes_pueden_anotarse(asistentes, eventos):
    se_puede_anotar = False
    for asistente in asistentes:
        eventos_a_asistir = asistente.obtener_eventos()
        for evento in eventos:
            se_puede_anotar = evento.se_puede_anotar(eventos_a_asistir)
            if se_puede_anotar:
                return se_puede_anotar            
    return se_puede_anotar

def asignar_asistentes(asistentes_organizados, eventos_mezclados):
    while(asistentes_pueden_anotarse(asistentes_organizados, eventos_mezclados)):
        for asistente in asistentes_organizados:
            for evento in eventos_mezclados:
                evento.anotar_asistente(asistente)

def imprimir_listado(eventos_mezclados, asistentes):
    for asistente in asistentes:
        print(f"{asistente.obtener_nombre()} tiene asignados los nombres de los siguientes eventos: {asistente.obtener_eventos()}")
    eventos_listados = [{evento.obtener_nombre(): (evento.obtener_inscriptos(), len(evento.obtener_inscriptos()))}  for evento in eventos_mezclados]
    print(eventos_listados)

if __name__ == "__main__":

    asistentes=["Luciano", "Julian", "Lucas", "Martín"]
    eventos= [
        Evento_exclusivo("Capitán América",(10,13),2), 
        Evento_exclusivo("Hulk",(10,11),1),
        Evento_exclusivo("Los 4 fantásticos",(11,12),3),
        Evento_exclusivo("Mujer Maravilla",(13,14),2), 
        Evento("Hombre araña",(16,17))
    ]

    #Mezclamos los eventos y asistenters
    asistentes_mezclados = mezclar(asistentes)
    eventos_mezclados = mezclar(eventos)

    #Generamos la lista ya con las instancias de la clase Asistente
    asistentes_organizados = organizar_asistentes(asistentes_mezclados)

    #Asignamos los asistentes a cada uno de los eventos hasta agotar cupo o ninguno pueda anotarse a mas eventos
    asignar_asistentes(asistentes_organizados, eventos_mezclados)

    #imprimimos el listado con la estructura esperada
    imprimir_listado(eventos_mezclados, asistentes_organizados)


