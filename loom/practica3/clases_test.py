from clases import Cliente
from persistencia import guardar_informacion, recuperar_informacion
from conversor import convertir_dicc_a_instancia
import unittest


class TestPersistencia(unittest.TestCase):

    def test_recuperar_json(self):
        metodo="json"
        cliente = Cliente("Pepito", dni=4154782045)
        guardar_informacion(cliente, metodo)
        cliente_recuperado = recuperar_informacion(metodo)
        self.assertEqual(str(cliente), str(cliente_recuperado))
    
    def test_recuperar_pickle(self):
        metodo="pickle"
        cliente = Cliente("Guillermo", dni=454545213)
        guardar_informacion(cliente, metodo)
        cliente_recuperado = recuperar_informacion(metodo)
        self.assertEqual(str(cliente), str(cliente_recuperado))

    def test_recuperar_shelve(self):
        metodo="shelve"
        cliente = Cliente("Facundo", dni=3945455455)
        guardar_informacion(cliente, metodo)
        cliente_recuperado = recuperar_informacion(metodo)
        self.assertEqual(str(cliente), str(cliente_recuperado))

if __name__ == "__main__":
    unittest.main()
