from data.tabelas_simples import TABELA_SIMPLES

def fator_r(folha, receita):
    return folha / receita if receita > 0 else 0

def anexo(fr):
    return "III" if fr >= 0.28 else "V"

def aliquota(rbt12, an):
    for f in TABELA_SIMPLES:
        if f["anexo"] == an and rbt12 <= f["max"]:
            return (rbt12 * f["aliquota"] - f["deducao"]) / rbt12

    # fallback de segurança (última faixa)
    ultima = [f for f in TABELA_SIMPLES if f["anexo"] == an][-1]
    return (rbt12 * ultima["aliquota"] - ultima["deducao"]) / rbt12


DAS_DETALHE = {
    "III": {
        "IRPJ": 0.04,
        "CSLL": 0.035,
        "PIS": 0.028,
        "COFINS": 0.1274,
        "CPP": 0.2885,
        "ISS": 0.4711,
    },
    "V": {
        "IRPJ": 0.055,
        "CSLL": 0.035,
        "PIS": 0.0305,
        "COFINS": 0.141,
        "CPP": 0.2785,
        "ISS": 0.46,
    }
}

def detalhar_das(valor_das, an):
    return {
        tributo: valor_das * perc
        for tributo, perc in DAS_DETALHE[an].items()
    }


