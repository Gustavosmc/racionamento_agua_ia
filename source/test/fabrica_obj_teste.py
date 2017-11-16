from source.racionamento_models import *
import random



def gerarConsumo(mult):
    consumos = []
    for i in range(23):
        consumos.append((i+1)*mult)

    return consumos

def gerarCliente(quantidade):
    clientes = []
    for i in range(quantidade):
        c = ClienteEssencial(random.randint(1, 3), "Cliente " + str(i), True)
        clientes.append(c)
    return clientes

def gerarBairros(quantidade, desc="Bairro"):
    bairros = []
    for i in range(quantidade):
        b = Bairro(desc + str(i),
                   random.randint(100, 1000),
                   gerarConsumo(random.randint(1, 10)),
                   gerarCliente(random.randint(1, 20)))
        bairros.append(b)
    return bairros

def gerarSetores(quantidade):
    setores = []
    for i in range(quantidade):
        s = Setor()
        for b in gerarBairros(random.randint(3, 10), ''.join(random.sample("ABCD", 4))):
            s.add_bairro(b)
            s.girar_aleatorio()
            s.restricao_hora_essencial((5,8), (18, 21))
        setores.append(s)
    return setores


def gerarEstados(quantidade):
    capacidade = 100000
    nivel = 30 # Por cento
    max_diario = 25000
    estados = []
    if quantidade % 2 != 0:
        print("Quantidade nao pode ser impar")
        return 0
    for i in range(quantidade):
        setores = gerarSetores(10)
        e = EstadoDia()
        e.capacidade_reservatorio, e.nivel_reservatorio, e.max_vol_diario = \
            capacidade, nivel, max_diario
        for s in setores:
            e.add_setor(s)
        estados.append(e)
    return estados