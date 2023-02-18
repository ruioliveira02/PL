from enum import Enum

class Sexo(Enum):
    MASCULINO = "M"
    FEMININO = "F"

class Pessoa:
    def __init__(self, idade, sexo, tensao, colestrol, batimento, temDoenca):
        self.idade = idade
        self.sexo = sexo
        self.tensao = tensao
        self.colestrol = colestrol
        self.batimento = batimento
        self.temDoenca = temDoenca

    def __str__(self):
        return f"{self.idade},{self.sexo.value},{self.tensao},{self.colestrol},{self.batimento},{self.temDoenca}"