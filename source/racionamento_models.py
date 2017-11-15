
from collections import namedtuple

ClienteEssencial = namedtuple('ClienteEssencial', 'nivel nome ativo')

class Bairro(object):

    def __init__(self, qtd_clientes=0, consumos=None, clientes_essenciais=None):
        self.qtd_clientes = qtd_clientes
        self.consumos = [0] * 24 if consumos is None else consumos
        self.clientes_essenciais = [] if clientes_essenciais is None else clientes_essenciais


class Setor(object):

    def __init__(self):
        self.total_clientes = 0
        self.total_consumos = [0] * 24
        self.ativo_horas = [0] * 24  # Genótipo
        self.bairros = []
        self.peso_clientes = 0

    def add_bairro(self, bairro):
        self.total_clientes += bairro.qtd_clientes
        self.peso_clientes += bairro.qtd_clientes
        for cs in bairro.clientes_essenciais:
            if cs.ativo:
                self.peso_clientes += (cs.nivel * 100)
        self.total_consumos = [x + y for x, y in zip(self.total_consumos, bairro.consumos)]
        self.bairros.append(bairro)

    def get_consumo_total(self):
        """
        :return: O consumo total de setor por dia
        """
        return sum(self.total_consumos)

    def get_consumo_total_hora(self):
        """
        :return: O consumo por cada hora ativa, que esse bairro estiver recebendo agua
        """
        cont = 0
        total = 0
        for ah in self.ativo_horas:
            if ah == 0:
                total += self.total_consumos[cont]
            cont += 0
        return total


    def restricao_hora_essencial(self, *args):
        """
        Torna todos os bits 0s para 1s onde é essencial o abastecimento de agua neste periodo
        :param Tuple (inicio, fim, intervalo) restricao hora abastecimento
        :return: None
        """
        for h in args:
            self.ativo_horas[h[0]:h[1]] = [1] * h[2]


class EstadoDia(object):

    def __init__(self):
        self.capacidade_reservatorio = 0
        self.nivel_reservatorio = 0
        self.maximo_vol_diario = 0

        self.setores = []
        self.ativo_horas = []
        self.aptidao = 0

    def add_setor(self, setor):
        self.setores.append(setor)
        self.ativo_horas.extend(setor.ativo_horas)

    def _set_aptidao(self):
        for setor in self.setores:
            cont = 0
            for h in setor.ativo_horas:
                if h == 0:
                    self.aptidao += setor.total_consumos[cont]
                cont += 1

