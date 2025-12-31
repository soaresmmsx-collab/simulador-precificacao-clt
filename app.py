import streamlit as st
import pandas as pd
from datetime import date

# ===============================
# AUTH (INALTERADO)
# ===============================
from auth.auth import login

# ===============================
# CORE – CLT
# ===============================
from core.clt import calcular_clt

# ===============================
# CORE – SIMPLES NACIONAL
# ===============================
from core.simples import (
    fator_r,
    anexo,
    aliquota,
    detalhar_das
)

# ===============================
# CORE – PRECIFICAÇÃO
# ===============================
from core.precificacao import calcular_precificacao

# ===============================
# IA
# ===============================
from core.ia_textos import (
    gerar_resumo_executivo,
    gerar_texto_comercial
)

# ===============================
# RELATÓRIOS
# ===============================
from core.relatorios import (
    gerar_proposta_comercial_pdf,
    gerar_pdf_tecnico
)

# ===============================
# CONFIG STREAMLIT
# ===============================
st.set_page_config(
    page_title="Simulador de Precificação CLT",
    layout="wide"
)

# ===============================
# LOGIN
# ===============================
if not login():
    st.stop()

st.title("📊 Simulador de Precificação CLT")

# =====================================================
# 1️⃣ IDENTIFICAÇÃO
# =====================================================
st.header("1️⃣ Identificação da Proposta")

c1, c2, c3 = st.columns(3)
cliente = c1.text_input("Cliente")
titulo_proposta = c2.text_input("Título da proposta", "Proposta de Prestação de Serviços")
validade = c3.text_input("Validade", "30 dias")

# =====================================================
# 2️⃣ CARGOS
# =====================================================
st.header("2️⃣ Estrutura de Cargos")

if "cargos" not in st.session_state:
    st.session_state.cargos = []

with st.expander("Adicionar cargo"):
    a, b, c = st.columns(3)
    cargo = a.text_input("Cargo")
    salario = b.number_input("Salário (R$)", min_value=0.0, step=100.0)
    qtd = c.number_input("Quantidade", min_value=1, step=1)

    if st.button("Adicionar cargo"):
        st.session_state.cargos.append({
            "Cargo": cargo,
            "Salário": salario,
            "Quantidade": qtd
        })

if st.session_state.cargos:
    st.dataframe(pd.DataFrame(st.session_state.cargos), use_container_width=True)
else:
    st.info("Nenhum cargo adicionado.")

# =====================================================
# 3️⃣ PARÂMETROS
# =====================================================
st.header("3️⃣ Parâmetros Financeiros")

p1, p2 = st.columns(2)
vale_refeicao = p1.number_input("Vale refeição por colaborador (R$)", value=600.0, step=50.0)
margem = p2.number_input("Margem de lucro (%)", value=20.0, step=1.0)

# =====================================================
# 4️⃣ IA
# =====================================================
st.header("4️⃣ Conteúdo da Proposta (IA)")

contexto = st.text_area(
    "Contexto da proposta",
    height=120,
    placeholder="Descreva o escopo, cliente e objetivos..."
)

x1, x2 = st.columns(2)
if x1.button("Gerar Resumo Executivo"):
    st.session_state.resumo_exec = gerar_resumo_executivo(contexto)

if x2.button("Gerar Texto Comercial"):
    st.session_state.texto_comercial = gerar_texto_comercial(contexto)

resumo_exec = st.text_area(
    "Resumo Executivo (editável)",
    st.session_state.get("resumo_exec", ""),
    height=180
)
st.markdown(resumo_exec)

texto_comercial = st.text_area(
    "Texto Comercial (editável)",
    st.session_state.get("texto_comercial", ""),
    height=260
)
st.markdown(texto_comercial)

# =====================================================
# 5️⃣ CÁLCULOS
# =====================================================
st.header("5️⃣ Resultados")

if st.button("Calcular Precificação"):
    if not st.session_state.cargos:
        st.error("Adicione ao menos um cargo.")
        st.stop()

    # ---------- CLT ----------
    clt_detalhado = {}
    folha_total = 0

    for cargo in st.session_state.cargos:
        detalhes, custo_unit = calcular_clt(
            cargo["Salário"],
            vale_refeicao
        )

        total_cargo = custo_unit * cargo["Quantidade"]
        folha_total += total_cargo

        for k, v in detalhes.items():
            clt_detalhado[k] = clt_detalhado.get(k, 0) + (v * cargo["Quantidade"])

    resultado_clt = {
        "folha_total": folha_total,
        "detalhado": clt_detalhado
    }

    # ---------- SIMPLES ----------
    # Receita simulada = custo + margem
    receita_base = folha_total * (1 + margem / 100)

    fr = fator_r(folha_total, receita_base)
    an = anexo(fr)
    aliq = aliquota(receita_base * 12, an)
    valor_das = receita_base * aliq
    das_detalhado = detalhar_das(valor_das, an)

    resultado_das = {
        "fator_r": fr,
        "anexo": an,
        "aliquota": aliq,
        "valor": valor_das,
        "detalhado": das_detalhado
    }

    # ---------- PRECIFICAÇÃO ----------
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

# =====================================================
# 6️⃣ OUTPUT
# =====================================================
if "resultado" in st.session_state:
    st.subheader("Resumo Financeiro")

    r = st.session_state.resultado

    a, b, c = st.columns(3)
    a.metric("Custo Total Mensal", f"R$ {r['precificacao']['custo_total']:,.2f}")
    b.metric("Lucro Mensal", f"R$ {r['precificacao']['lucro']:,.2f}")
    c.metric("Valor da Nota Fiscal", f"R$ {r['precificacao']['valor_nf']:,.2f}")

    st.header("6️⃣ Relatórios")

    y1, y2 = st.columns(2)

    if y1.button("📄 Proposta Comercial (PDF)"):
        gerar_proposta_comercial_pdf(
            "proposta_comercial.pdf",
            cliente,
            titulo_proposta,
            resumo_exec,
            "",
            texto_comercial,
            validade,
            f"R$ {r['precificacao']['valor_nf']:,.2f}",
            f"{margem}%",
            st.session_state.cargos
        )
        with open("proposta_comercial.pdf", "rb") as f:
            st.download_button("⬇️ Baixar PDF Comercial", f, "proposta_comercial.pdf")

    if y2.button("📑 Proposta Técnica (PDF)"):
        gerar_pdf_tecnico(
            "proposta_tecnica.pdf",
            st.session_state.cargos,
            r["clt"]["detalhado"],
            r["das"]["valor"],
            r["precificacao"]["lucro"],
            r["das"]["detalhado"]
        )
        with open("proposta_tecnica.pdf", "rb") as f:
            st.download_button("⬇️ Baixar PDF Técnico", f, "proposta_tecnica.pdf")
