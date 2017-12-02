from source.racionamento_models import *
from random import random, choice

import copy
class RacionamentoAG():

    def __init__(self, estados=None):
        self.estados = estados
        self.estados_filhos = []

    def proxima_geracao(self):
        self.estados_filhos = []
        for i in range((int(len(self.estados) / 2))):
            vencedor1, vencedor2 = (self._torneio(choice(self.estados), choice(self.estados)),
                                    self._torneio(choice(self.estados), choice(self.estados)))
            filho1, filho2 = self._crossover(vencedor1, vencedor2)
            self.estados_filhos.append(filho1)
            self.estados_filhos.append(filho2)
        self._elitismo()
        self.estados.clear()
        self.estados.extend(self.estados_filhos)

    def _mutacao(self, *args):
        for estado in args:
            for i in range(len(estado.setores) * HORAS):
                percent = random()
                if percent < FATOR_MUTACAO:
                    v = estado.ativo_horas[i]
                    estado.ativo_horas[i] = 0 if v == 1 else 1

    def _mutacao2(self, *args):
        for estado in args:
            percent = random()
            if percent < 0.1:
                aux_sets = []
                for i in range(0, len(estado.setores) * HORAS, HORAS):
                    aux_set = Setor()
                    aux_set.set_ativo_horas(estado.ativo_horas[i: i + HORAS])
                    aux_sets.append(aux_set)
                aux_sets.sort(key=lambda x: x.get_cont_ativos())
                for s, auxs in zip(estado.setores, aux_sets):
                    s.set_ativo_horas(auxs.ativo_horas)

    def _crossover(self, pai1, pai2):
        """
        :param outro_estado: Outro objeto EstadoDia
        :return: Uma tupla contendo 2 filhos EstadoDia
        """
        filho1, filho2 = deepcopy(pai1), deepcopy(pai1)
        filho1.ativo_horas.clear()
        filho2.ativo_horas.clear()

        ponto_corte = 1
        controle = True
        for i in range(0, len(pai1.ativo_horas), ponto_corte):
            if controle:
                filho1.ativo_horas.extend(pai1.ativo_horas[i:i + ponto_corte])
                filho2.ativo_horas.extend(pai2.ativo_horas[i:i + ponto_corte])
                controle = False
            else:
                filho1.ativo_horas.extend(pai2.ativo_horas[i:i + ponto_corte])
                filho2.ativo_horas.extend(pai1.ativo_horas[i:i + ponto_corte])
                controle = True

        cont = 0
        for set1, set2 in zip(filho1.setores, filho2.setores):
            set1.set_ativo_horas(filho1.ativo_horas[cont: cont + HORAS])
            set2.set_ativo_horas(filho2.ativo_horas[cont: cont + HORAS])
            filho1.ativo_horas[cont: cont + HORAS] = set1.ativo_horas
            filho2.ativo_horas[cont: cont + HORAS] = set2.ativo_horas
            cont += HORAS

        self._mutacao(filho1, filho2)
        return filho1, filho2


    def _torneio(self, est1, est2):
        return est1 if est1.get_aptidao() <= est2.get_aptidao() else est2


    def _elitismo(self):
        self.estados.sort(key=lambda x: x.get_aptidao(), reverse=True)
        self.estados_filhos.sort(key=lambda x: x.get_aptidao(), reverse=True)
        if self.estados_filhos[-1].get_aptidao() > self.estados[0].get_aptidao():
            self.estados_filhos[-1] = deepcopy(self.estados[0])


    def __repr__(self):
        ret = ''
        cont = 1
        for estado in self.estados:
            ret += "Estado: " + str(cont) + "\n"
            ret += str(estado) + str(estado.get_aptidao()) + "\n"
            ret += "Economia de água : {}\n".format(estado.get_economia_agua())
            ret += "Consumo Total : {}\n".format(estado.get_consumo_total_hora())
            cont += 1
        ret += '\n-------------------------------------------------------------\n'
        return ret