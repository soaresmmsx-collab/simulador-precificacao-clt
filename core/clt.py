ENCARGOS = {
    "INSS Patronal": 0.20,
    "RAT": 0.01,
    "FGTS": 0.08,
    "FGTS adicional": 0.032,
    "13º salário": 0.0833,
    "Férias": 0.1111,
    "1/3 constitucional": 0.037
}

def calcular_clt(salario, beneficio):
    detalhes = {}
    total_encargos = 0

    for nome, perc in ENCARGOS.items():
        valor = salario * perc
        detalhes[nome] = valor
        total_encargos += valor

    custo_total = salario + total_encargos + beneficio
    return detalhes, custo_total
