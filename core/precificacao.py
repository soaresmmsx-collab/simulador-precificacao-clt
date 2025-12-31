def precificar(custo, margem):
    preco = custo / (1 - margem)
    lucro = preco - custo
    return preco, lucro
