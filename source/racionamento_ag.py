from source.racionamento_models import *
import random as rd
import copy
class RacionamentoAG():

    def __init__(self, estados=None):
        self.estados = estados
        self.estados_filhos = []

    def proxima_geracao(self):
        self.estados_filhos = []
        for i in range((int(len(self.estados) / 2))):
            vencedor1, vencedor2 = (self._torneio(rd.choice(self.estados), rd.choice(self.estados)),
                                    self._torneio(rd.choice(self.estados), rd.choice(self.estados)))
            filho1, filho2 = vencedor1.crossover(vencedor2)
            self.estados_filhos.append(filho1)
            self.estados_filhos.append(filho2)
        self.estados.clear()
        self.estados.extend(self.estados_filhos)

    def _torneio(self, est1, est2):
        return est1 if est1.get_aptidao() <= est2.get_aptidao() else est2

    def __repr__(self):
        ret = ''
        cont = 1
        for estado in self.estados:
            ret += "Estado: " + str(cont) + "\n"
            ret += str(estado) + str(estado.get_aptidao()) + "\n"
            cont += 1
        ret += '\n-------------------------------------------------------------\n'
        return ret