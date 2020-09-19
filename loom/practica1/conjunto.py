class Conjunto:

    def __init__(self, valores):
        self.__conjunto = self.__eliminar_duplicados(valores)

    def obtener_valor(self):
        return self.__conjunto

    def __eliminar_duplicados(self, lista):
        lista_sin_duplicados = []
        for elemento in lista:
            if elemento not in lista_sin_duplicados:
                lista_sin_duplicados.append(elemento)
        return lista_sin_duplicados

    def __union(self, conjuntoA, conjuntoB):
        return self.__eliminar_duplicados(conjuntoA + conjuntoB)

    def __interseccion(self, conjuntoA, conjuntoB):
        conjunto_interseccion = []
        for elemento in conjuntoB:
            if elemento in conjuntoA and elemento not in conjunto_interseccion:
                conjunto_interseccion.append(elemento)
            
        return conjunto_interseccion        
    
    def union(self, conjuntoB):
        return self.__union(self.__conjunto, conjuntoB.obtener_valor())

    def interseccion(self, conjuntoB):        
        return self.__interseccion(self.__conjunto, conjuntoB.obtener_valor())

    def diferencia(self, conjuntoB):
        return [elemento for elemento in self.__conjunto if elemento not in conjuntoB.obtener_valor()]
    
    def diferencia_asimetrica(self, conjuntoB):    
        return self.__union(self.diferencia(b), conjuntoB.diferencia(a)) 
        
    def __repr__(self):
        return self.__conjunto
    
a = Conjunto([1,2])
b = Conjunto([2,3])

print(a.union(b))
print(a.interseccion(b))
print(a.diferencia(b))
print(a.diferencia_asimetrica(b))