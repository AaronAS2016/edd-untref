import unittest
from covid import EstadisticaCovid
import pathlib

datos_esperados_casos_por_provincia = {
    "CABA": {"F": 0, "M": 1, "NR": 0},
    "Buenos Aires":  {"F": 0, "M": 1, "NR": 0},
    "Córdoba": {"F": 1, "M": 1, "NR": 0},
    "Mendoza": {"F": 2, "M": 0, "NR": 0}
}

datos_esperados_casos_por_rango_etario = {
    "0-20": 2,
    "20-40": 1,
    "40-60": 2,
    "60+": 1,
    "Sin informacion": 0
}

datos_esperados_por_promedio_edad = {
    "CABA": {"promedio": 53.0, "cantidad": 1},
    "Buenos Aires":  {"promedio": 21.0, "cantidad": 1},
    "Córdoba": {"promedio": 52.5, "cantidad": 2},
    "Mendoza": {"promedio": 2.5, "cantidad": 2}
}

datos_esperados_por_cantidad_de_casos = [
    ("Córdoba", 2),
    ("Mendoza", 2),
    ("CABA", 1),
    ("Buenos Aires", 1)
]

ubicacion_archivo = f"{pathlib.Path(__file__).parent.absolute()}/test.csv"


class TestEstadisticaCovid(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__covid = EstadisticaCovid(ubicacion_archivo)
        self.__covid.comenzar_analisis()

    def test_comprobar_existencia_de_datos(self):
        resultados = self.__covid.obtener_resultados()
        self.assertIsNotNone(resultados)

    def test_casos_esperados_por_provincia_separados_por_genero(self):
        resultados = self.__covid.obtener_resultados()[
            "cantidad_casos_por_provincia"]
        self.assertEqual(resultados, datos_esperados_casos_por_provincia)

    def test_casos_esperados_por_rango_etario(self):
        resultados = self.__covid.obtener_resultados(
        )["cantidad_casos_por_rango_etario"]
        self.assertEqual(resultados, datos_esperados_casos_por_rango_etario)

    def test_casos_esperados_por_edad_promedio(self):
        resultados = self.__covid.obtener_resultados()[
            "promedio_edad_infectado"]
        self.assertEqual(resultados, datos_esperados_por_promedio_edad)

    def test_casos_esperados_mayores_por_provincia(self):
        resultados = self.__covid.obtener_resultados()[
            "provincias_con_mayor_casos"]
        self.assertEqual(resultados, datos_esperados_por_cantidad_de_casos)


if __name__ == "__main__":
    unittest.main()
