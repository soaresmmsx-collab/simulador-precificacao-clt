import pandas as pd
import streamlit as st

def exportar(df):
    st.download_button(
        "⬇️ Exportar CSV",
        df.to_csv(index=False).encode("utf-8"),
        "custos.csv",
        "text/csv"
    )

    excel = df.to_excel(index=False)
