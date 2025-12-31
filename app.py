import streamlit as st
import pandas as pd
from io import BytesIO

from auth.auth import login
from ui.inputs import cargos
from core.clt import calcular_clt
from core.precificacao import precificar
from core.simples import fator_r, anexo, aliquota, detalhar_das
from core.utils import brl
from core.relatorios import gerar_proposta_comercial_pdf, gerar_pdf_tecnico
from core.ia_textos import gerar_resumo_executivo, gerar_texto_comercial

# -------------------- Login --------------------
if "logged" not in st.session_state:
    st.session_state["logged"] = False
if not st.session_state["logged"]:
    login()
    st.stop()

st.title("Simulador de Precificação CLT + Simples Nacional")

# -------------------- 1) Identificação --------------------
st.header("1) Identificação da Proposta")
cliente = st.text_input("Cliente")
titulo_proposta = st.text_input("Título da proposta", "Proposta de Prestação de Serviços")
validade = st.text_input("Validade", "30 dias")

# -------------------- 2) Estratégia (IA) --------------------
st.header("2) Estratégia da Proposta (IA)")
tom_ia = st.selectbox("Tom da narrativa", ["Executivo", "Comercial"])
contexto = st.text_area("Contexto base para a IA", height=120)

if "resumo_exec" not in st.session_state:
    st.session_state["resumo_exec"] = ""
if "texto_comercial" not in st.session_state:
    st.session_state["texto_comercial"] = ""

c1, c2 = st.columns(2)
with c1:
    if st.button("Gerar resumo executivo"):
        st.session_state["resumo_exec"] = gerar_resumo_executivo(contexto, tom_ia)
with c2:
    if st.button("Gerar texto comercial"):
        st.session_state["texto_comercial"] = gerar_texto_comercial(contexto, tom_ia)

resumo_exec = st.text_area("Resumo executivo (editável)", st.session_state["resumo_exec"], height=120)
texto_comercial = st.text_area("Texto comercial (editável)", st.session_state["texto_comercial"], height=200)

# -------------------- 3) Estrutura de Custos --------------------
st.header("3) Estrutura de Custos")
lista_cargos = cargos()

# -------------------- 4) Parâmetros Financeiros --------------------
st.header("4) Parâmetros Financeiros")
vale = st.number_input("Vale alimentação por colaborador (R$)", min_value=0.0, value=600.0)
margem = st.slider("Margem de lucro sobre a RECEITA (%)", 1, 50, 20) / 100

# -------------------- 5) Cálculos --------------------
tabela_cargos = []
total_clt = {}
custo_total = 0.0
folha_anual = 0.0

for nome, salario, qtd in lista_cargos:
    if not nome or salario <= 0 or qtd <= 0:
        continue
    detalhes, custo_unit = calcular_clt(salario, vale)
    for k, v in detalhes.items():
        total_clt[k] = total_clt.get(k, 0) + v*qtd
    custo_total += custo_unit*qtd
    folha_anual += custo_unit*qtd*12
    tabela_cargos.append({
        "Cargo": nome, "Quantidade": qtd,
        "Salário Base": salario, "Benefícios": vale,
        **detalhes, "Custo Unitário": custo_unit, "Custo Total": custo_unit*qtd
    })

preco_nf, lucro = precificar(custo_total, margem)
fr = fator_r(folha_anual, preco_nf*12)
an = anexo(fr)
aliq = aliquota(preco_nf*12, an)
das = preco_nf*aliq
das_det = detalhar_das(das, an)

# -------------------- 6) Resultados --------------------
st.header("5) Resultados Consolidados")
st.write("Valor mensal da proposta:", brl(preco_nf))
st.write("Lucro mensal:", brl(lucro))
st.write("Fator R:", f"{fr:.2%}")
st.write("Anexo:", an)
st.write("Alíquota efetiva:", f"{aliq:.2%}")
st.write("DAS mensal:", brl(das))

# -------------------- Tabela / Exportações --------------------
st.subheader("Custos detalhados por cargo")
df = pd.DataFrame(tabela_cargos)
st.dataframe(df)

st.download_button("CSV", df.to_csv(index=False).encode("utf-8"),
                   "custos_detalhados.csv", "text/csv")

buf = BytesIO()
with pd.ExcelWriter(buf, engine="openpyxl") as w:
    df.to_excel(w, index=False)
buf.seek(0)
st.download_button("Excel", buf,
                   "custos_detalhados.xlsx",
                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# -------------------- 7) Relatórios --------------------
st.header("6) Relatórios")
if st.button("Gerar Proposta COMERCIAL (PDF)"):
    gerar_proposta_comercial_pdf(
        "proposta_comercial.pdf",
        cliente,
        titulo_proposta,
        resumo_exec,
        "Texto institucional configurável no app.",
        texto_comercial,
        validade,
        brl(preco_nf),
        f"{margem*100:.2f}%",
        tabela_cargos
    )
    with open("proposta_comercial.pdf","rb") as f:
        st.download_button("Baixar Proposta Comercial", f, "proposta_comercial.pdf","application/pdf")

if st.button("Gerar Proposta TÉCNICA (PDF)"):
    gerar_pdf_tecnico(
        "proposta_tecnica.pdf",
        tabela_cargos,
        total_clt,
        brl(das),
        brl(lucro),
        {k: brl(v) for k,v in das_det.items()}
    )
    with open("proposta_tecnica.pdf","rb") as f:
        st.download_button("Baixar Proposta Técnica", f, "proposta_tecnica.pdf","application/pdf")
