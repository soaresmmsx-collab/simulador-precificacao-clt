from data.tabelas_simples import TABELA_SIMPLES

def fator_r(folha_anual, receita_anual):
    return folha_anual / receita_anual if receita_anual > 0 else 0

def definir_anexo(fr):
    return "III" if fr >= 0.28 else "V"

def aliquota_efetiva(rbt12, anexo):
    for f in TABELA_SIMPLES:
        if f["anexo"] == anexo and f["min"] <= rbt12 <= f["max"]:
            return (rbt12 * f["aliquota"] - f["deducao"]) / rbt12
    return 0
