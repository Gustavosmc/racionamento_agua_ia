

class ClienteEspecial(object):

    def __init__(self):
        self.nivel = 0
        self.nome = ''
        self.ativo = False


class Bairro(object):

    def __int__(self):
        self.total_clientes = 0
        self.maior_consumo = 0
        self.maior_consumo_dom_fer = 0
        self.maior_consumo_sabado = 0
        self.clientes_especiais = []


class Regiao(object):

    def __init__(self):
        self.total_clientes = 0
        self.total_maior_consumo = 0
        self.total_maior_consumo_dom_fer = 0
        self.total_maior_consumo_sabado = 0
        self.bairros = []


class Racionamento(object):

    def __init__(self):
        self.capacidade_reservatorio = 0
        self.nivel_reservatorio = 0
        self.maximo_vol_diario = 0
        self.regioes = []



