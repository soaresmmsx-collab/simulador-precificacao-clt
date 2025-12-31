import streamlit as st
import pandas as pd
from datetime import date

# ===============================
# IMPORTS DO CORE (REAIS)
# ===============================
from auth.auth import login

from core.clt import calcular_clt
from core.simples import calcular_das_simples
from core.precificacao import calcular_precificacao

from core.ia_textos import (
    gerar_resumo_executivo,
    gerar_texto_comercial
)

from core.relatorios import (
    gerar_proposta_comercial_pdf,
    gerar_pdf_tecnico
)

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Simulador de Precificação CLT",
    layout="wide"
)

# ===============================
# LOGIN (INALTERADO)
# ===============================
if not login():
    st.stop()

st.title("📊 Simulador de Precificação CLT")

# ===============================
# IDENTIFICAÇÃO DA PROPOSTA
# ===============================
st.header("1️⃣ Identificação da Proposta")

col1, col2, col3 = st.columns(3)
cliente = col1.text_input("Cliente")
titulo_proposta = col2.text_input(
    "Título da proposta",
    "Proposta de Prestação de Serviços"
)
validade = col3.text_input("Validade", "30 dias")

# ===============================
# ESTRUTURA DE CARGOS
# ===============================
st.header("2️⃣ Estrutura de Cargos")

if "cargos" not in st.session_state:
    st.session_state.cargos = []

with st.expander("Adicionar cargo"):
    c1, c2, c3 = st.columns(3)
    cargo = c1.text_input("Cargo")
    salario = c2.number_input("Salário (R$)", min_value=0.0, step=100.0)
    quantidade = c3.number_input("Quantidade", min_value=1, step=1)

    if st.button("Adicionar cargo"):
        st.session_state.cargos.append({
            "Cargo": cargo,
            "Salário": salario,
            "Quantidade": quantidade
        })

if st.session_state.cargos:
    st.dataframe(
        pd.DataFrame(st.session_state.cargos),
        use_container_width=True
    )
else:
    st.info("Nenhum cargo adicionado.")

# ===============================
# PARÂMETROS FINANCEIROS
# ===============================
st.header("3️⃣ Parâmetros Financeiros")

col1, col2 = st.columns(2)
vale_refeicao = col1.number_input(
    "Vale refeição por colaborador (R$)",
    value=600.0,
    step=50.0
)
margem = col2.number_input(
    "Margem de lucro (%)",
    value=20.0,
    step=1.0
)

# ===============================
# IA — CONTEÚDO DA PROPOSTA
# ===============================
st.header("4️⃣ Conteúdo da Proposta (IA)")

contexto = st.text_area(
    "Contexto da proposta (base para IA)",
    height=120,
    placeholder="Descreva o escopo, o cliente e os objetivos da proposta..."
)

col1, col2 = st.columns(2)
if col1.button("Gerar Resumo Executivo"):
    st.session_state.resumo_exec = gerar_resumo_executivo(contexto)

if col2.button("Gerar Texto Comercial"):
    st.session_state.texto_comercial = gerar_texto_comercial(contexto)

# ===============================
# RESUMO EXECUTIVO
# ===============================
resumo_exec = st.text_area(
    "Resumo Executivo (editável)",
    value=st.session_state.get("resumo_exec", ""),
    height=180
)

st.markdown("**Pré-visualização formatada:**")
st.markdown(resumo_exec)

# ===============================
# TEXTO COMERCIAL
# ===============================
texto_comercial = st.text_area(
    "Texto Comercial (editável)",
    value=st.session_state.get("texto_comercial", ""),
    height=260
)

st.markdown("**Pré-visualização formatada:**")
st.markdown(texto_comercial)

# ===============================
# CÁLCULOS
# ===============================
st.header("5️⃣ Resultados")

if st.button("Calcular Precificação"):
    if not st.session_state.cargos:
        st.error("Adicione ao menos um cargo.")
        st.stop()

    # ===============================
    # CÁLCULO CLT (USANDO core/clt.py REAL)
    # ===============================
    detalhes_clt_consolidado = {}
    folha_total = 0

    for cargo in st.session_state.cargos:
        salario = cargo["Salário"]
        quantidade = cargo["Quantidade"]

        detalhes_unit, custo_unit = calcular_clt(
            salario,
            vale_refeicao
        )

        custo_total_cargo = custo_unit * quantidade
        folha_total += custo_total_cargo

        for nome, valor in detalhes_unit.items():
            detalhes_clt_consolidado[nome] = (
                detalhes_clt_consolidado.get(nome, 0)
                + (valor * quantidade)
            )

    resultado_clt = {
        "detalhado": detalhes_clt_consolidado,
        "folha_total": folha_total
    }

    # ===============================
    # SIMPLES NACIONAL / DAS
    # ===============================
    resultado_das = calcular_das_simples(folha_total)

    # ===============================
    # PRECIFICAÇÃO FINAL
    # ===============================
    resultado_precificacao = calcular_precificacao(
        resultado_clt,
        resultado_das,
        margem
    )

    st.session_state.resultado = {
        "clt": resultado_clt,
        "das": resultado_das,
        "precificacao": resultado_precificacao
    }

# ===============================
# OUTPUT E RELATÓRIOS
# ===============================
if "resultado" in st.session_state:
    st.subheader("Resumo Financeiro")

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Custo Total Mensal",
        f"R$ {st.session_state.resultado['precificacao']['custo_total']:,.2f}"
    )
    col2.metric(
        "Lucro Mensal",
        f"R$ {st.session_state.resultado['precificacao']['lucro']:,.2f}"
    )
    col3.metric(
        "Valor da Nota Fiscal",
        f"R$ {st.session_state.resultado['precificacao']['valor_nf']:,.2f}"
    )

    st.header("6️⃣ Relatórios")

    col1, col2 = st.columns(2)

    if col1.button("📄 Gerar Proposta Comercial (PDF)"):
        gerar_proposta_comercial_pdf(
            "proposta_comercial.pdf",
            cliente,
            titulo_proposta,
            resumo_exec,
            "",  # texto institucional fixo (se houver)
            texto_comercial,
            validade,
            f"R$ {st.session_state.resultado['precificacao']['valor_nf']:,.2f}",
            f"{margem}%",
            st.session_state.cargos
        )

        with open("proposta_comercial.pdf", "rb") as f:
            st.download_button(
                "⬇️ Baixar Proposta Comercial",
                f,
                "proposta_comercial.pdf",
                mime="application/pdf"
            )

    if col2.button("📑 Gerar Proposta Técnica (PDF)"):
        gerar_pdf_tecnico(
            "proposta_tecnica.pdf",
            st.session_state.cargos,
            st.session_state.resultado["clt"]["detalhado"],
            st.session_state.resultado["das"]["total"],
            st.session_state.resultado["precificacao"]["lucro"],
            st.session_state.resultado["das"]["detalhado"]
        )

        with open("proposta_tecnica.pdf", "rb") as f:
            st.download_button(
                "⬇️ Baixar Proposta Técnica",
                f,
                "proposta_tecnica.pdf",
                mime="application/pdf"
            )
