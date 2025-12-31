ENCARGOS_CLT = 0.70  # fixo conforme planilha

def custo_unitario_clt(salario, beneficio):
    encargos = salario * ENCARGOS_CLT
    return salario + encargos + beneficio
