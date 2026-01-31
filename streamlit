

import streamlit as st
import pandas as pd
import plotly.express as px

Configuração da página

st.set_page_config(
page_title="Dashboard de Salários na Área de Dados",
page_icon="📊",
layout="wide",
)

Carregamento dos dados

df = pd.read_csv(
"https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
)

Sidebar

st.sidebar.header("🔍 Filtros")

anos = sorted(df["ano"].unique())
anos_sel = st.sidebar.multiselect("Ano", anos, default=anos)

senioridades = sorted(df["senioridade"].unique())
senioridades_sel = st.sidebar.multiselect(
"Senioridade", senioridades, default=senioridades
)

contratos = sorted(df["contrato"].unique())
contratos_sel = st.sidebar.multiselect(
"Tipo de Contrato", contratos, default=contratos
)

tamanhos = sorted(df["tamanho_empresa"].unique())
tamanhos_sel = st.sidebar.multiselect(
"Tamanho da Empresa", tamanhos, default=tamanhos
)

Filtragem

df_f = df[
(df["ano"].isin(anos_sel)) &
(df["senioridade"].isin(senioridades_sel)) &
(df["contrato"].isin(contratos_sel)) &
(df["tamanho_empresa"].isin(tamanhos_sel))
]

Conteúdo principal

st.title("🎲 Dashboard de Salários na Área de Dados")

if df_f.empty:
st.warning("Nenhum dado para os filtros selecionados.")
st.stop()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Salário médio", f"${df_f['usd'].mean():,.0f}")
col2.metric("Salário máximo", f"${df_f['usd'].max():,.0f}")
col3.metric("Registros", df_f.shape[0])
col4.metric("Cargo mais frequente", df_f["cargo"].mode()[0])

st.markdown("---")

Gráficos

colg1, colg2 = st.columns(2)

with colg1:
top = (
df_f.groupby("cargo")["usd"]
.mean()
.nlargest(10)
.sort_values()
.reset_index()
)
fig = px.bar(top, x="usd", y="cargo", orientation="h")
st.plotly_chart(fig, use_container_width=True)

with colg2:
fig2 = px.histogram(df_f, x="usd", nbins=30)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Dados Detalhados")
st.dataframe(df_f)
