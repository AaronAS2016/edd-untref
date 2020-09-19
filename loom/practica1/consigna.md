# Consigna
Se quieren implementar las operaciones posibles entre conjuntos, utilizando listas en python. Para ello se te pide que implementes la clase Conjunto, con métodos para cada una de las siguientes operaciones:
    1. Unión
    2. Intersección
    3. Diferencia
    4. Diferencia simétrica

Ejemplos:

```
>>> a = Conjunto([1, 2])
>>> b = Conjunto([2, 3])
>>> a.union b
[1, 2, 3]
>>> a.interseccion(b)
[2]
>>> a.diferencia(b)
[1]
>>> a.diferencia_simetrica(b)
[1, 3]
```

Importante: Recordá que una de las características de los conjuntos es que no tiene duplicados.