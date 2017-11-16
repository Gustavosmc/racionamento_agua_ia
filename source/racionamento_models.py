
from collections import namedtuple
from copy import deepcopy
from random import randint, random

ClienteEssencial = namedtuple('ClienteEssencial', 'nivel nome ativo')

HORAS = 23

class Bairro(object):

    def __init__(self, nome, qtd_clientes=0, consumos=None, clientes_essenciais=None):
        self.nome = nome
        self.qtd_clientes = qtd_clientes
        self.consumos = [0] * HORAS if consumos is None else consumos
        self.clientes_essenciais = [] if clientes_essenciais is None else clientes_essenciais


class Setor(object):

    def __init__(self):
        """
        :param total_consumos, vetor de consumos por hora em m3
        """
        self.total_clientes = 0
        self.total_consumos = [0] * HORAS
        self.ativo_horas = [0] * HORAS  # Genótipo
        self.bairros = []
        self.peso_clientes = 0
        self.restricoes_hora = []

    def add_bairro(self, bairro):
        self.total_clientes += bairro.qtd_clientes
        self.peso_clientes += bairro.qtd_clientes
        for cs in bairro.clientes_essenciais:
            if cs.ativo:
                self.peso_clientes += (cs.nivel * 100)
        self.total_consumos = [x + y for x, y in zip(self.total_consumos, bairro.consumos)]
        self.bairros.append(bairro)

    def set_ativo_horas(self, vet):
        if len(vet) == HORAS:
            self.ativo_horas = vet
        if len(self.restricoes_hora) > 0:
            for h in self.restricoes_hora:
                self.ativo_horas[h[0]:h[1]] = [1] * (h[1] - h[0])

    def get_consumo_total(self):
        """
        :return: O consumo total de setor por dia
        """
        return sum(self.total_consumos)

    def get_consumo_total_hora(self):
        """
        :return: O consumo por cada hora ativa, que esse bairro estiver recebendo agua
        """
        cont, total = 0, 0
        for ah in self.ativo_horas:
            if ah == 1:
                total += self.total_consumos[cont]
            cont += 1
        return total

    def get_clientes_hora(self):
        cont, total = 0, 0
        for ah in self.ativo_horas:
            if ah == 1:
                total += self.total_clientes
            cont += 1
        return total

    def girar_aleatorio(self):
        """
        Torna o genoma binario desse setor aleatorio
        :return:
        """
        for i in range(len(self.ativo_horas)):
            self.ativo_horas[i] = randint(0,1)


    def restricao_hora_essencial(self, *args):
        """
        Torna todos os bits 0s para 1s onde é essencial o abastecimento de agua neste periodo
        :param Tuple (inicio, fim, intervalo) restricao hora abastecimento
        :return: None
        """

        for h in args:
            self.restricoes_hora.append(tuple(h))
            self.ativo_horas[h[0]:h[1]] = [1] * (h[1] - h[0])

    def __radd__(self, other):
        other = other.get_consumo_total_hora() if isinstance(other, Setor) else other
        return self.get_consumo_total_hora() + other

    def __lt__(self, other):
        return self.peso_clientes < other.peso_clientes

class EstadoDia(object):

    def __init__(self):
        self.capacidade_reservatorio = 0
        self.nivel_reservatorio = 0
        self.max_vol_diario = 0

        self.consumo_total = 0
        self.setores = []
        self.ativo_horas = []  # Genotipo


    def add_setor(self, setor):
        self.setores.append(setor)
        self.ativo_horas.extend(setor.ativo_horas)
        self.consumo_total += setor.get_consumo_total()

    def set_max_vol_diario(self, volume):
        self.max_vol_diario = volume

    def get_consumo_total_hora(self):
        return sum(self.setores)

    def get_aptidao(self):
        total_clientes_hora = sum(x.get_clientes_hora() for x in self.setores)
        return self.get_consumo_total_hora()

    def _mutacao(self):
        for i in range(len(self.setores) * HORAS):
            percent = random()
            if percent < 0.03:
                v = self.ativo_horas[i]
                self.ativo_horas[i] = 1 if v == 0 else 0


    def crossover(self, outro_estado):
        """
        :param outro_estado: Outro objeto EstadoDia
        :return: Uma tupla contendo 2 filhos EstadoDia
        """
        filho1, filho2 = deepcopy(self), deepcopy(self)
        filho1.ativo_horas.clear()
        filho2.ativo_horas.clear()

        ponto_corte = 1
        for i in range(0, len(self.ativo_horas), ponto_corte):
            if i % 2 == 0:
                filho1.ativo_horas.append(self.ativo_horas[i])
                filho2.ativo_horas.append(outro_estado.ativo_horas[i])
            else:
                filho1.ativo_horas.append(outro_estado.ativo_horas[i])
                filho2.ativo_horas.append(self.ativo_horas[i])

        self._mutacao()
        cont = 0
        for set1, set2 in zip(filho1.setores, filho2.setores):
            set1.set_ativo_horas(filho1.ativo_horas[cont: cont+HORAS])
            set2.set_ativo_horas(filho2.ativo_horas[cont: cont+HORAS])
            filho1.ativo_horas[cont: cont+HORAS] = set1.ativo_horas
            filho2.ativo_horas[cont: cont+HORAS] = set2.ativo_horas
            cont += 23

        return filho1, filho2


    def __repr__(self):
        ret = ""
        cont = 1
        for s in self.setores:
            ret += ("Setor " + str(cont))
            ret += " horas :" + str(s.ativo_horas) + "\n"
            cont += 1
        ret += "\n\n"
        return ret

