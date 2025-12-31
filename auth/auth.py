import streamlit as st
import hashlib

USERS = {
    "max": "681fae29b727e172cd8605c3444ec059c2340c9ae5941a9e9ecc46c0081db7c8"
}

def _hash(p):
    return hashlib.sha256(p.encode()).hexdigest()

def login():
    st.title("🔐 Login")
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if u in USERS and USERS[u] == _hash(p):
            st.session_state.logged = True
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")
