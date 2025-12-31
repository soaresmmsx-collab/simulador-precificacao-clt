import streamlit as st
from auth.auth import login
from ui.inputs import coletar_cargos
from core.clt import custo_unitario_clt
from core.precificacao import preco_com_margem
from core.simples import fator_r, definir_anexo, aliquota_efetiva
from core.utils import brl

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    login()
    st.stop()

st.title("📊 Sistema de Precificação CLT + Simples Nacional")

vale = st.number_input("Vale Alimentação por colaborador (R$)", value=600.0)
margem = st.slider("Margem de lucro (%)", 1, 50) / 100

cargos = coletar_cargos()

custo_total = 0
folha_anual = 0

for nome, salario, qtd in cargos:
    custo_u = custo_unitario_clt(salario, vale)
    custo_total += custo_u * qtd
    folha_anual += custo_u * qtd * 12

preco_nf, lucro_total = preco_com_margem(custo_total, margem)

fr = fator_r(folha_anual, preco_nf * 12)
anexo = definir_anexo(fr)
aliq = aliquota_efetiva(preco_nf * 12, anexo)
das = preco_nf * aliq

st.subheader("📈 Resultado Consolidado")
st.write("Nota Fiscal Mensal:", brl(preco_nf))
st.write("Lucro Líquido Mensal:", brl(lucro_total))
st.write("DAS:", brl(das))
st.write("Fator R:", f"{fr:.2%}")
st.write("Anexo Simples:", anexo)
