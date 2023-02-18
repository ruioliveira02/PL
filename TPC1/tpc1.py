"""
Todos os exercicios foram realizados, incluindo
a criacao de graficos (barras e circulares)
recorrendo a matplotlib
"""

import re
from pessoa import Pessoa, Sexo
from distribuicao import Distribuicao

def __parse_line__(line):
    match = re.search("(\d+),(M|F),(\d+),(\d+),(\d+),(0|1)", line)

    if not match:
        raise ValueError(f"Invalid CSV line: {line}")

    (idade, sexo, tensao, colestrol, batimento, temDoenca) = match.groups()
    return Pessoa(int(idade), Sexo(sexo), int(tensao), int(colestrol), int(batimento),
                  temDoenca == "1")

def parse_csv(file):
    ans = []
    with open(file) as f:
        f.readline() #Ignorar cabecalho do CSV
        for line in f:
            ans.append(__parse_line__(line))

    return ans

def doenca_por_sexo(pessoas):
    n = len(pessoas)
    pontos = {"M": 0.0, "F": 0.0}

    for pessoa in pessoas:
        ch = pessoa.sexo.value
        pontos[ch] += 1 if pessoa.temDoenca else 0

    # Assumindo que ha pelo menos 1 pessoa de cada sexo
    # senao nao faz sentido calcular a percentagem
    pontos["M"] /= n
    pontos["F"] /= n

    dist = Distribuicao({}, "Doença por Sexo", "Sexo", "% Doença (Do Total)")
    dist.add_ponto((0,pontos["M"]), "M")
    dist.add_ponto((1,pontos["F"]), "F")
    return dist

def doenca_por_idade(pessoas):
    pontos = {}
    n = len(pessoas)

    for pessoa in pessoas:
        grupo = pessoa.idade // 5
        if grupo not in pontos:
            pontos[grupo] = 0

        pontos[grupo] += 1 if pessoa.temDoenca else 0

    dist = Distribuicao({}, "Doença Por Idade", "Idade", "% (Doente do Total)")
    for grupo in pontos:
        dist.add_ponto((grupo,pontos[grupo] / n), f"[{grupo * 5}-{grupo * 5 + 4}]")

    return dist

def doenca_por_colestrol(pessoas):
    n = len(pessoas)
    minGroup = 1e18
    maxGroup = -1
    for pessoa in pessoas:
        minGroup = min(minGroup, pessoa.colestrol // 10)
        maxGroup = max(maxGroup, pessoa.colestrol // 10)

    pontos = {}
    for i in range(minGroup, maxGroup + 1):
        pontos[i] = 0

    for pessoa in pessoas:
        grupo = pessoa.colestrol // 10

        pontos[grupo] += 1 if pessoa.temDoenca else 0

    dist = Distribuicao({}, "Doença por Colestrol", "Colestrol", "Doente (% do Total)")
    for grupo in pontos:
        dist.add_ponto((grupo,pontos[grupo] / n),
                       f"[{grupo * 10}-{grupo * 10 + 9}]")

    return dist

def main():
    pessoas = parse_csv("myheart.csv")
    print("Escolha a distribuicao a calcular")
    print("I: Por Idade")
    print("S: Por Sexo")
    print("C: Por Colestrol")
    x = input()
    dist = None
    if x == "I":
        dist = doenca_por_idade(pessoas)
    elif x == "S":
        dist = doenca_por_sexo(pessoas)
    elif x == "C":
        dist = doenca_por_colestrol(pessoas)
    else:
        print("Invalid Input")
        return

    print(dist.to_table())
    print("Escolha o tipo de grafico")
    print("B: Barras")
    print("C: Circular")
    x = input()
    if x == "B":
        dist.to_bar_chart()
    elif x == "C":
        dist.to_pie_chart()
    else:
        print("Invalid Input")
        return

if __name__ != "main":
    main()