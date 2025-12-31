import streamlit as st
import pandas as pd
from io import BytesIO

from auth.auth import login
from ui.inputs import cargos
from core.clt import calcular_clt
from core.precificacao import precificar
from core.simples import fator_r, anexo, aliquota, detalhar_das
from core.utils import brl
from core.relatorios import gerar_pdf_comercial, gerar_pdf_tecnico

# ======================================================
# LOGIN
# ======================================================
if "logged" not in st.session_state:
    st.session_state["logged"] = False

if not st.session_state["logged"]:
    login()
    st.stop()

# ======================================================
# INTERFACE – INPUTS
# ======================================================
st.title("Sistema de Precificação CLT + Simples Nacional")

vale = st.number_input(
    "Vale Alimentação por colaborador (R$)",
    value=600.0,
    min_value=0.0
)

margem = st.slider(
    "Margem de lucro sobre a RECEITA (%)",
    min_value=1,
    max_value=50,
    value=20
) / 100

lista_cargos = cargos()

st.subheader("📄 Dados da Proposta")

cliente = st.text_input("Cliente")
titulo_proposta = st.text_input("Título da proposta", "Proposta de prestação de serviços")
descricao_proposta = st.text_area(
    "Descrição da proposta (escopo resumido)",
    height=150
)
validade = st.text_input("Validade da proposta", "30 dias")


# ======================================================
# CÁLCULOS
# ======================================================
tabela_cargos = []
total_clt_detalhado = {}

custo_total = 0.0
folha_anual = 0.0

for nome, salario, qtd in lista_cargos:
    if not nome or salario <= 0 or qtd <= 0:
        continue

    detalhes_clt, custo_unit = calcular_clt(salario, vale)

    # acumula CLT detalhado
    for encargo, valor in detalhes_clt.items():
        total_clt_detalhado[encargo] = (
            total_clt_detalhado.get(encargo, 0.0) + valor * qtd
        )

    custo_total += custo_unit * qtd
    folha_anual += custo_unit * qtd * 12

    tabela_cargos.append({
        "Cargo": nome,
        "Quantidade": qtd,
        "Salário Base": salario,
        **detalhes_clt,
        "Benefícios": vale,
        "Custo Unitário": custo_unit,
        "Custo Total": custo_unit * qtd
    })

# Se não houver cargos válidos, não prossegue
if not tabela_cargos:
    st.warning("Informe ao menos um cargo válido para continuar.")
    st.stop()

# ======================================================
# PRECIFICAÇÃO
# ======================================================
preco_nf, lucro = precificar(custo_total, margem)

fr = fator_r(folha_anual, preco_nf * 12)
an = anexo(fr)

aliq = aliquota(preco_nf * 12, an)
das = preco_nf * aliq
das_detalhado = detalhar_das(das, an)

# ======================================================
# TABELA DETALHADA POR CARGO
# ======================================================
st.subheader("📊 Custos detalhados por cargo")

df = pd.DataFrame(tabela_cargos)
st.dataframe(df)

# ======================================================
# EXPORTAÇÕES
# ======================================================
st.subheader("📤 Exportar custos detalhados")

# CSV
st.download_button(
    "⬇️ Exportar CSV",
    df.to_csv(index=False).encode("utf-8"),
    "custos_detalhados_por_cargo.csv",
    "text/csv"
)

# Excel
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Custos")

excel_buffer.seek(0)

st.download_button(
    "⬇️ Exportar Excel",
    excel_buffer,
    "custos_detalhados_por_cargo.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ======================================================
# RESULTADO CONSOLIDADO
# ======================================================
st.subheader("📈 Resultado Consolidado")

st.write("💰 **Nota Fiscal Mensal:**", brl(preco_nf))
st.write("📉 **Custo Total Mensal:**", brl(custo_total))
st.write("📈 **Lucro Líquido Mensal:**", brl(lucro))

st.write("📊 **Fator R:**", f"{fr:.2%}")
st.write("📑 **Anexo Simples Nacional:**", an)
st.write("🧾 **Alíquota Efetiva:**", f"{aliq:.2%}")

st.write("🧾 **DAS Total Mensal:**", brl(das))

# ======================================================
# DAS DETALHADO
# ======================================================
st.subheader("🧾 DAS – Detalhamento por tributo")

for tributo, valor in das_detalhado.items():
    st.write(f"{tributo}:", brl(valor))

# ======================================================
# PROPOSTAS (PDF)
# ======================================================
st.subheader("📄 Propostas em PDF")

if st.button("📄 Gerar Proposta COMERCIAL (PDF)"):
    gerar_pdf_comercial(
        "proposta_comercial.pdf",
        brl(preco_nf),
        f"{margem * 100:.2f}%",
        tabela_cargos
    )

    with open("proposta_comercial.pdf", "rb") as f:
        st.download_button(
            "⬇️ Baixar Proposta Comercial",
            f,
            "proposta_comercial.pdf",
            "application/pdf"
        )

if st.button("📄 Gerar Proposta TÉCNICA (PDF)"):
    gerar_pdf_tecnico(
        "proposta_tecnica.pdf",
        tabela_cargos,
        total_clt_detalhado,
        brl(das),
        brl(lucro)
    )

    with open("proposta_tecnica.pdf", "rb") as f:
        st.download_button(
            "⬇️ Baixar Proposta Técnica",
            f,
            "proposta_tecnica.pdf",
            "application/pdf"
        )
