import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv(
    "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
)

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

anos_disponiveis = sorted(df["ano"].unique())
anos_selecionados = st.sidebar.multiselect(
    "Ano", anos_disponiveis, default=anos_disponiveis
)

senioridades_disponiveis = sorted(df["senioridade"].unique())
senioridades_selecionadas = st.sidebar.multiselect(
    "Senioridade", senioridades_disponiveis, default=senioridades_disponiveis
)

contratos_disponiveis = sorted(df["contrato"].unique())
contratos_selecionados = st.sidebar.multiselect(
    "Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis
)

tamanhos_disponiveis = sorted(df["tamanho_empresa"].unique())
tamanhos_selecionados = st.sidebar.multiselect(
    "Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis
)

# --- Filtragem do DataFrame ---
df_filtrado = df[
    (df["ano"].isin(anos_selecionados))
    & (df["senioridade"].isin(senioridades_selecionadas))
    & (df["contrato"].isin(contratos_selecionados))
    & (df["tamanho_empresa"].isin(tamanhos_selecionados))
]

# --- Conteúdo Principal ---
st.title("🎲 Dashboard de Salários na Área de Dados")

if df_filtrado.empty:
    st.warning("Nenhum dado para os filtros selecionados.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${df_filtrado['usd'].mean():,.0f}")
col2.metric("Salário máximo", f"${df_filtrado['usd'].max():,.0f}")
col3.metric("Total de registros", df_filtrado.shape[0])
col4.metric("Cargo mais frequente", df_filtrado["cargo"].mode()[0])

st.markdown("---")

# --- Gráficos ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    'top_cargos' = (
        df_filtrado.groupby("cargo")["usd"]
        .mean()
        .nlargest(10)
        .sort_values()
        .reset_index()
    'fig_cargos' = px.bar(
        top_cargos,
        x="usd",
        y="cargo",
        orientation="h",
        title="Top 10 cargos por salário médio",
        labels={"usd": "Média salarial anual (USD)", "cargo": ""},
    )
    st.plotly_chart(fig_cargos, use_container_width=True)

with col_graf2:
    fig_hist = px.histogram(
        df_filtrado,
        x="usd",
        nbins=30,
        title="Distribuição de salários anuais",
        labels={"usd": "Faixa salarial (USD)"},
    )
    st.plotly_chart(fig_hist, use_container_width=True)

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    remoto_contagem = df_filtrado["remoto"].value_counts().reset_index()
    remoto_contagem.columns = ["tipo_trabalho", "quantidade"]
    fig_remoto = px.pie(
        remoto_contagem,
        names="tipo_trabalho",
        values="quantidade",
        title="Proporção dos tipos de trabalho",
        hole=0.5,
    )
    st.plotly_chart(fig_remoto, use_container_width=True)

with col_graf4:
    df_ds = df_filtrado[df_filtrado["cargo"] == "Data Scientist"]
    media_ds_pais = df_ds.groupby("residencia_iso3")["usd"].mean().reset_index()
    fig_paises = px.choropleth(
        media_ds_pais,
        locations="residencia_iso3",
        color="usd",
        title="Salário médio de Cientista de Dados por país",
        labels={"usd": "Salário médio (USD)", "residencia_iso3": "País"},
    )
    st.plotly_chart(fig_paises, use_container_width=True)

# --- Tabela ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
