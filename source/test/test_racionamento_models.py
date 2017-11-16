import unittest
from source.test.fabrica_obj_teste import *

from source.racionamento_models import *

class TestSetor(unittest.TestCase):

    def test_addBairro(self):
        cs1 = ClienteEssencial(1, "Creche", True)
        b = Bairro("Bairro1", qtd_clientes=120, consumos=gerarConsumo(1), clientes_essenciais=[cs1])
        b1 = Bairro("Bairro2", qtd_clientes=120, consumos=gerarConsumo(2), clientes_essenciais=[])
        self.assertEqual(b.consumos[0], 1)
        self.assertEqual(b.consumos[1], 2)
        s = Setor()
        self.assertEqual(len(s.total_consumos), 23)
        s.add_bairro(b)
        s.add_bairro(b1)
        s.restricao_hora_essencial((5, 8, 3), (18, 22, 4))
        self.assertEqual(s.get_consumo_total(), 828)
        self.assertEqual(s.get_consumo_total_hora(), 309)
        self.assertEqual(s.total_clientes, 240)
        self.assertEqual(s.peso_clientes, 340)
        self.assertEqual(s.total_consumos[2], 9)
        self.assertEqual(len(s.bairros), 2)


class TestEstadoDia(unittest.TestCase):

    def test_addSetor(self):
        cs1 = ClienteEssencial(1, "Creche", True)
        b = Bairro("Bairro 1", qtd_clientes=120, consumos=gerarConsumo(1), clientes_essenciais=[cs1])
        b1 = Bairro("Bairro 2", qtd_clientes=120, consumos=gerarConsumo(2), clientes_essenciais=[])
        s = Setor()
        s.add_bairro(b)
        s.add_bairro(b1)
        cs2 = ClienteEssencial(2, "Escola", True)
        b = Bairro("Bairro 3", qtd_clientes=200, consumos=gerarConsumo(3), clientes_essenciais=[cs1])
        b1 = Bairro("Bairro 4", qtd_clientes=200, consumos=gerarConsumo(4), clientes_essenciais=[cs2])
        s1 = Setor()
        s1.add_bairro(b)
        s1.add_bairro(b1)
        estadoDia = EstadoDia()
        estadoDia.add_setor(s)
        estadoDia.add_setor(s1)
        self.assertEqual(len(estadoDia.ativo_horas), 46)
        self.assertEqual(len(estadoDia.setores), 2)
        s.restricao_hora_essencial((5, 8), (18, 22))
        s1.restricao_hora_essencial((5, 8), (18, 22))


    def test_crossover(self):
        import copy
        cs1 = ClienteEssencial(1, "Creche", True)
        b = Bairro("Bairro 1", qtd_clientes=120, consumos=gerarConsumo(10), clientes_essenciais=[cs1])
        b1 = Bairro("Bairro 2", qtd_clientes=120, consumos=gerarConsumo(10), clientes_essenciais=[])
        s = Setor()
        s.add_bairro(b)
        s.add_bairro(b1)
        cs2 = ClienteEssencial(2, "Escola", True)
        b = Bairro("Bairro 3", qtd_clientes=200, consumos=gerarConsumo(10), clientes_essenciais=[cs1])
        b1 = Bairro("Bairro 4", qtd_clientes=200, consumos=gerarConsumo(10), clientes_essenciais=[cs2])
        s1 = Setor()
        s1.add_bairro(b)
        s1.add_bairro(b1)
        estadoDia = EstadoDia()
        estadoDia.add_setor(s)
        estadoDia.add_setor(s1)
        estadoDia1 = EstadoDia()
        s3 = copy.deepcopy(s1)
        s3.restricao_hora_essencial((1, 4))
        s4 = copy.deepcopy(s1)
        s4.restricao_hora_essencial((4, 6))
        estadoDia1.add_setor(s4)
        estadoDia1.add_setor(s3)
        print(estadoDia, estadoDia1)
        print(estadoDia1.get_consumo_total_hora())

        e1, e2 = estadoDia.crossover(estadoDia1)

        print(e1, e2)
        print(e1.get_consumo_total_hora())
        print(e2.get_consumo_total_hora())

