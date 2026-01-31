pandas==2.2.3
streamlit==1.44.1
plotly==5.24.1
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

df = pd.read_csv(
    "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
)

st.sidebar.header("🔍 Filtros")

anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect(
    "Ano", anos_disponiveis, default=anos_disponiveis
)
