from persistencia import guardar_informacion, recuperar_informacion
from clases import Cliente
from excepciones import NoHayUsuarioCreadoError
from random import randrange


def guardar_usuario(metodo, clientes):
    cliente_a_guardar = clientes[randrange(len(clientes))]
    instancia_a_guardar = Cliente(
        cliente_a_guardar["nombre"], cliente_a_guardar["dni"])
    print("Cliente a guardar:")
    print(instancia_a_guardar)
    guardar_informacion(instancia_a_guardar, metodo)


def recuperar_informacion_en_disco(metodo):
    try:
        informacion = recuperar_informacion(metodo)
        print(f"Cliente guardado en disco como {metodo} es: \n{informacion}")
    except NoHayUsuarioCreadoError as e:
        print("Ups")
        print(e)


if __name__ == "__main__":
    clientes = [
        {"nombre": "Pepito el pistolero", "dni": "7877435226"},
        {"nombre": "Pepita la pistolera", "dni": "4141226638"},
        {"nombre": "Hernan el peluquero", "dni": "5376324131"},
        {"nombre": "Fabian el ayudante", "dni": "2111878766"},
        {"nombre": "Chapulin colonisman", "dni": "5825211515"},
    ]

    respuesta_usuario = True
    opcion_salida = '7'

    while(respuesta_usuario != opcion_salida):
        print("""

======= Persistencia de datos =================

1.Guardar nuevo estudiante aleatorio en Pickle 
2.Guardar nuevo estudiante aleatorio en JSON
3.Guardar nuevo estudiante aleatorio en Shelve
4.Recuperar estudiante aleatorio en Pickle
5.Recuperar estudiante aleatorio en JSON
6.Recuperar estudiante aleatorio en Shelve
7.Salir
        """)
        respuesta_usuario = input("Que te gustaria hacer? ")
        if respuesta_usuario == "1":
            guardar_usuario(metodo="pickle", clientes=clientes)
        elif respuesta_usuario == "2":
            guardar_usuario(metodo="json", clientes=clientes)
        elif respuesta_usuario == "3":
            guardar_usuario(metodo="shelve", clientes=clientes)
        elif respuesta_usuario == "4":
            recuperar_informacion_en_disco(metodo="pickle")
        elif respuesta_usuario == "5":
            recuperar_informacion_en_disco(metodo="json")
        elif respuesta_usuario == "6":
            recuperar_informacion_en_disco(metodo="shelve")
        elif respuesta_usuario == "7":
            print("Saliendo...")
        elif respuesta_usuario != "":
            print("\n Opcion invalida")
