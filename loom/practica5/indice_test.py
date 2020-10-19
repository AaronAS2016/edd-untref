import unittest
from main import IndiceNovelas
from excepciones import NoSeEncontroPalabra

class TestIndiceInvertido(unittest.TestCase):

    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        self._indice = IndiceNovelas("test.txt", novelas=[
            "LA BUENAVENTURA",
            "LA CORNETA DE LLAVES",
            "LAS DOS GLORIAS",
            "EL AFRANCESADO",
            "¡VIVA EL PAPA!",
            "EL EXTRANJERO",
            "EL LIBRO TALONARIO",
            "MOROS Y CRISTIANOS",
            "EL AÑO EN SPITZBERG"
        ])


    def _testear_busqueda_de_palabra(self, resultado_esperado, palabra):
        resultado = self._indice.buscar(palabra)
        self.assertEquals(resultado_esperado, resultado)
    
    def test_buscar_palabra_agosto(self):
        resultado_esperado = {'agosto'}, {'LA BUENAVENTURA', 'EL AÑO EN SPITZBERG'}
        self._testear_busqueda_de_palabra(resultado_esperado, "Agosto")

    def test_buscar_palabra_con_numeros(self):
        resultado_esperado = {'1816'}, {'LA BUENAVENTURA'}
        self._testear_busqueda_de_palabra(resultado_esperado, "1816")

    def test_buscar_palabra_con_comodin(self):
        resultado_esperado = {'abrazarlo', 'abrazo'}, {'LAS DOS GLORIAS', 'LA BUENAVENTURA'}
        self._testear_busqueda_de_palabra(resultado_esperado, "abra*")
    
    def test_buscar_palabra_que_no_esta_en_el_indice(self):
        with self.assertRaises(NoSeEncontroPalabra): self._indice.buscar("palabraquenoestaenelindiceporqueesmuyfacha")


if __name__ == "__main__":
    unittest.main()




