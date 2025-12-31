import streamlit as st

def cargos():
    lista = []
    n = st.number_input("Quantidade de cargos", 1, step=1)
    for i in range(n):
        st.subheader(f"Cargo {i+1}")
        nome = st.text_input("Nome", key=f"n{i}")
        sal = st.number_input("Salário", 0.0, key=f"s{i}")
        qtd = st.number_input("Qtd", 1, key=f"q{i}")
        lista.append((nome, sal, qtd))
    return lista
