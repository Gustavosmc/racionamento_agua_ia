from source.racionamento_models import *

def gerarConsumo(seed):
    consumos = []
    for i in range(24):
        consumos.append(i*seed)

    return consumos