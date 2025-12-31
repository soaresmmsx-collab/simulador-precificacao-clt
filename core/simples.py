from data.tabelas_simples import TABELA_SIMPLES

def fator_r(folha, receita):
    return folha / receita if receita > 0 else 0

def anexo(fr):
    return "III" if fr >= 0.28 else "V"

def aliquota(rbt12, an):
    for f in TABELA_SIMPLES:
        if f["anexo"] == an and f["min"] <= rbt12 <= f["max"]:
            return (rbt12*f["aliquota"] - f["deducao"]) / rbt12
    return 0
