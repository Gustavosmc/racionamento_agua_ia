import unittest
from source.test.fabrica_obj_teste import *

from source.racionamento_ag import *

class TestRacionamentoGA(unittest.TestCase):

    def testGerarEstados(self):
        self.assertEqual(gerarEstados(3), 0)

        estados = gerarEstados(2)


    def testEvolucao(self):
        rodadas = 100
        estados = gerarEstados(20)
        racionamento_ag = RacionamentoAG(estados=estados)
        melhor = racionamento_ag.estados[0]
        while melhor.get_aptidao() > melhor.max_vol_diario:
            print(racionamento_ag)
            racionamento_ag.proxima_geracao()
            melhor = racionamento_ag.estados[0]
