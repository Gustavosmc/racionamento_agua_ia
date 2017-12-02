import unittest
from source.test.fabrica_obj_teste import *

from source.racionamento_ag import *

class TestRacionamentoGA(unittest.TestCase):

    def testGerarEstados(self):
        self.assertEqual(gerarEstados(3), 0)

        estados = gerarEstados(2)


    def testEvolucao(self):
        rodadas = 200
        estados = gerarEstados(40)
        racionamento_ag = RacionamentoAG(estados=estados)
        melhor = racionamento_ag.estados[0]
        for i in range(rodadas):
            print(racionamento_ag)
            racionamento_ag.proxima_geracao()
            melhor = racionamento_ag.estados[0]
