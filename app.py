import streamlit as st
from auth.auth import login
from ui.inputs import cargos
from core.clt import calcular_clt
from core.precificacao import precificar
from core.simples import fator_r, anexo, aliquota
from core.utils import brl
import pandas as pd

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    login()
    st.stop()

st.title("Sistema de Precificação CLT + Simples")

vale = st.number_input("Vale Alimentação", 600.0)
margem = st.slider("Margem (%)", 1, 50) / 100

dados = []
custo_total = 0
folha_anual = 0

for nome, salario, qtd in cargos():
    det, custo = calcular_clt(salario, vale)
    custo_total += custo*qtd
    folha_anual += custo*qtd*12
    dados.append({
        "Cargo": nome,
        "Custo unitário": custo,
        "Quantidade": qtd
    })

preco, lucro = precificar(custo_total, margem)
fr = fator_r(folha_anual, preco*12)
an = anexo(fr)
aliq = aliquota(preco*12, an)
das = preco*aliq

st.subheader("Resultado")
st.write("Nota Fiscal:", brl(preco))
st.write("Lucro:", brl(lucro))
st.write("DAS:", brl(das))
st.write("Fator R:", f"{fr:.2%}")
st.write("Anexo:", an)

df = pd.DataFrame(dados)
st.dataframe(df)
