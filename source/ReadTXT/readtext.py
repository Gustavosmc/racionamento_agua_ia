from source.racionamento_models import *
import random
from source.test.fabrica_obj_teste import *
import os

def ler_setores(dir_file):
    i = 0
    file = open(dir_file).read()
    line = file.split('Bairros:')
    totalRegioes = len(line)
    setores = []
    for i in range(1, totalRegioes):
        print("*************************************************")
        linha = line[i].split(',')
        # print('Região',i,"Qtde de bairros =",len(linha))
        setor = Setor()
        for x in range(len(linha)):
            bairro = Bairro(linha[x].lstrip(), randint(20, 300), gerarConsumo(10), gerarCliente(randint(0, 5)))
            setor.add_bairros(bairro)
        setores.append(setor)
    return setores
    # print("Total de Regiões:",totalRegioes,"\nTotal de Bairros:",totalBairros)

