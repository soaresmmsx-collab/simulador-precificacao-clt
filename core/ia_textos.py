from core.ia_textos import (
    gerar_resumo_executivo,
    gerar_texto_comercial
)

# ------------------------------------
# IA AVANÇADA
# ------------------------------------
st.subheader("🤖 Conteúdo Gerado por IA")

tom_ia = st.selectbox(
    "Tom da narrativa",
    ["Executivo", "Comercial"]
)

contexto = st.text_area(
    "Contexto da proposta (base para IA)",
    height=120
)

if "resumo_exec" not in st.session_state:
    st.session_state["resumo_exec"] = ""

if "texto_comercial" not in st.session_state:
    st.session_state["texto_comercial"] = ""

col1, col2 = st.columns(2)

with col1:
    if st.button("Gerar resumo executivo"):
        st.session_state["resumo_exec"] = gerar_resumo_executivo(contexto, tom_ia)

with col2:
    if st.button("Gerar texto comercial"):
        st.session_state["texto_comercial"] = gerar_texto_comercial(contexto, tom_ia)

resumo_exec = st.text_area(
    "Resumo executivo (editável)",
    st.session_state["resumo_exec"],
    height=120
)

texto_comercial = st.text_area(
    "Texto comercial (editável)",
    st.session_state["texto_comercial"],
    height=200
)
