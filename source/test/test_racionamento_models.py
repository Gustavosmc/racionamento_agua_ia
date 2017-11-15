import unittest
from source.test.fabrica_obj_teste import *

from source.racionamento_models import *

class TestSetor(unittest.TestCase):

    def test_addBairro(self):
        cs1 = ClienteEssencial(1, "Creche", True)
        b = Bairro(qtd_clientes=120, consumos=gerarConsumo(1), clientes_essenciais=[cs1])
        b1 = Bairro(qtd_clientes=120, consumos=gerarConsumo(2), clientes_essenciais=[])
        self.assertEqual(b.consumos[0], 0)
        self.assertEqual(b.consumos[1], 1)
        s = Setor()
        self.assertEqual(len(s.total_consumos), 24)
        s.add_bairro(b)
        s.add_bairro(b1)
        self.assertEqual(s.total_clientes, 240)
        self.assertEqual(s.peso_clientes, 340)
        self.assertEqual(s.total_consumos[2], 6)
        self.assertEqual(len(s.bairros), 2)


class TestEstadoDia(unittest.TestCase):

    def test_addSetor(self):
        cs1 = ClienteEssencial(1, "Creche", True)
        b = Bairro(qtd_clientes=120, consumos=gerarConsumo(1), clientes_essenciais=[cs1])
        b1 = Bairro(qtd_clientes=120, consumos=gerarConsumo(2), clientes_essenciais=[])
        s = Setor()
        s.add_bairro(b)
        s.add_bairro(b1)
        cs2 = ClienteEssencial(2, "Escola", True)
        b = Bairro(qtd_clientes=200, consumos=gerarConsumo(3), clientes_essenciais=[cs1])
        b1 = Bairro(qtd_clientes=200, consumos=gerarConsumo(4), clientes_essenciais=[cs2])
        s1 = Setor()
        s1.add_bairro(b)
        s1.add_bairro(b1)
        estadoDia = EstadoDia()
        estadoDia.add_setor(s)
        estadoDia.add_setor(s1)
        self.assertEqual(len(estadoDia.ativo_horas), 48)
        self.assertEqual(len(estadoDia.setores), 2)
