# Consigna
Se dispone de un [archivo de valores separados por comas que contiene información sobre los casos de COVID19](https://datos.gob.ar/dataset/salud-covid-19-casos-registrados-republica-argentina/archivo/salud_fd657d02-a33a-498b-a91b-2ef1a68b8d16) registrados en el país.

Dado que el archivo es muy extenso como para abrirlo y analizarlo en Excel, se prefirió realizar un programa en Python que pueda responder con complejidad __*O(n)*__, y evitando recorrer el archivo más de una vez, las siguientes estadísticas de interés:

1. Cantidad de casos por provincia, separados por género
2. Cantidad de casos por rango etario (0 a 20, 20 a 40, 40 a 60, 60 o más)
3. Promedio de edad de los infectados por provincia
4. Provincias ordenadas por cantidad de casos, con los casos

Toda esta información deberá presentarse en forma de tablas, en cuatro archivos diferentes (cada uno corresponde a los puntos anteriores, no se piden 16 salidas distintas).

1. Archivo con campos de longitud fija
2. Archivo con campos de longitud fija
3. Archivo con campos de longitud variable
4. Archivo con campos de longitud variable