import streamlit as st

def coletar_cargos():
    cargos = []
    n = st.number_input("Quantidade de cargos", min_value=1, step=1)

    for i in range(n):
        st.subheader(f"Cargo {i+1}")
        nome = st.text_input("Nome", key=f"nome_{i}")
        salario = st.number_input("Salário", min_value=0.0, key=f"sal_{i}")
        qtd = st.number_input("Quantidade", min_value=1, step=1, key=f"qtd_{i}")
        cargos.append((nome, salario, qtd))

    return cargos
