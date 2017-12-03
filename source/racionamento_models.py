from collections import namedtuple
from copy import deepcopy
from random import randint, random
from operator import attrgetter

ClienteEssencial = namedtuple('ClienteEssencial', 'nivel nome ativo')

HORAS = 23
MULT_PESO_CLIENTE = 100
FATOR_MUTACAO = 0.01


class Bairro(object):
    def __init__(self, nome, qtd_clientes=0, consumos=None, clientes_essenciais=None):
        self.nome = nome
        self.qtd_clientes = qtd_clientes
        self.consumos = [0] * HORAS if consumos is None else consumos
        self.clientes_essenciais = [] if clientes_essenciais is None else clientes_essenciais

    def __repr__(self):
        return str(self.nome).replace("\n", "")


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
        self.max_vol_diario = 0
        self.restricoes_hora = []


    def get_cont_ativos(self):
        cont = 0
        for i in self.ativo_horas:
            cont += i
        return cont

    def get_aptidao(self):
        aptidao = abs(self.get_consumo_total_hora() - self.max_vol_diario)
        # retornar menor valor possivel

        return aptidao

    def add_bairro(self, bairro):
        self.total_clientes += bairro.qtd_clientes
        self.peso_clientes += bairro.qtd_clientes
        for cs in bairro.clientes_essenciais:
            if cs.ativo:
                self.peso_clientes += (MULT_PESO_CLIENTE * cs.nivel)
        self.total_consumos = [x + y for x, y in zip(self.total_consumos, bairro.consumos)]
        self.bairros.append(bairro)

    def add_bairros(self, *args):
        for b in args:
            self.add_bairro(b)

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

    def get_peso_clientes(self):
        return self.peso_clientes if self.peso_clientes > 0 else 1

    def get_consumo_total_hora(self):
        """
        :return: O consumo por cada hora ativa, que esse bairro estiver recebendo agua
        """
        cont, total = 0, 0
        for ah in self.ativo_horas:
            if ah == 1:
                total += self.total_consumos[cont]
            cont += 1
        return total if total > 0 else 1

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
            self.ativo_horas[i] = randint(0, 1)

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
        self.setores.sort(key=attrgetter('peso_clientes'))
        hr = self.setores.index(setor) * HORAS
        if hr > len(self.ativo_horas):
            self.ativo_horas.extend(setor.ativo_horas)
        else:
            self.ativo_horas[hr: hr] = setor.ativo_horas
        self.consumo_total += setor.get_consumo_total()
        # redistribui cada vez que um setor é adicionado a porcentagem de agua
        self.distribuir_max_vol_diario()

    def distribuir_max_vol_diario(self):
        for setor in self.setores:
            porcentagem_peso = (setor.get_peso_clientes() * 100) / self.get_peso_total()
            setor.max_vol_diario = self.max_vol_diario * (porcentagem_peso / 100)


    def set_max_vol_diario(self, volume):
        self.max_vol_diario = volume

    def get_consumo_total_hora(self):
        return sum(self.setores)

    def get_maior_peso(self):
        return max(x.get_peso_clientes() for x in self.setores)

    def get_peso_total(self):
        return sum(x.get_peso_clientes() for x in self.setores)

    def get_economia_agua(self):
        return self.consumo_total - self.get_consumo_total_hora()

    def get_aptidao(self):
        # total_clientes_hora = sum(x.get_clientes_hora() for x in self.setores)
        aptidao_total = sum(x.get_aptidao() for x in self.setores)
        return aptidao_total

    def __repr__(self):
        ret = ""
        cont = 1
        for s in self.setores:
            ret += "Setor {}: Racionamento {}\n               " \
                   "Consumo {}\n               " \
                   "Cidades {}\n               " \
                   "Detalhes ConsumoMax/Gasto: {:.0f}/{} , Peso: {} , Total Clientes: {}\n\n" \
                   "".format(cont, str(s.ativo_horas), s.total_consumos, s.bairros,
                             s.max_vol_diario, s.get_consumo_total_hora(),
                             s.peso_clientes, s.total_clientes)
            cont += 1
        ret += "\n\n"
        return ret
