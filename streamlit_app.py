import streamlit_app.py
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados com Cache ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
    return pd.read_csv(url)

df = load_data()

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Função auxiliar para multiselect para evitar repetição de código
def create_filter(label, column):
    options = sorted(df[column].unique())
    return st.sidebar.multiselect(label, options, default=options)

anos_selecionados = create_filter("Ano", "ano")
senioridades_selecionadas = create_filter("Senioridade", "senioridade")
contratos_selecionados = create_filter("Tipo de Contrato", "contrato")
tamanhos_selecionados = create_filter("Tamanho da Empresa", "tamanho_empresa")

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
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Tente ajustar os filtros na barra lateral.")
    st.stop()

# Métricas Principais
col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio Anual", f"US$ {df_filtrado['usd'].mean():,.0f}")
col2.metric("Salário Máximo", f"US$ {df_filtrado['usd'].max():,.0f}")
col3.metric("Total de Registros", df_filtrado.shape[0])
col4.metric("Cargo mais Frequente", df_filtrado["cargo"].mode()[0])

st.markdown("---")

# --- Gráficos: Linha 1 ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    top_cargos = (
        df_filtrado.groupby("cargo")["usd"]
        .mean()
        .nlargest(10)
        .sort_values(ascending=True)
        .reset_index()
    )
    fig_cargos = px.bar(
        top_cargos,
        x="usd",
        y="cargo",
        orientation="h",
        title="Top 10 Cargos por Salário Médio",
        labels={"usd": "Média Salarial (USD)", "cargo": ""},
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_cargos, use_container_width=True)

with col_graf2:
    fig_hist = px.histogram(
        df_filtrado,
        x="usd",
        nbins=30,
        title="Distribuição de Salários Anuais",
        labels={"usd": "Faixa Salarial (USD)"},
        color_discrete_sequence=['#636EFA']
    )
    fig_hist.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist, use_container_width=True)

# --- Gráficos: Linha 2 ---
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    remoto_contagem = df_filtrado["remoto"].value_counts().reset_index()
    remoto_contagem.columns = ["tipo_trabalho", "quantidade"]
    fig_remoto = px.pie(
        remoto_contagem,
        names="tipo_trabalho",
        values="quantidade",
        title="Proporção dos Tipos de Trabalho",
        hole=0.5,
    )
    st.plotly_chart(fig_remoto, use_container_width=True)

with col_graf4:
    # Verificação para evitar erro caso não existam Data Scientists no filtro
    df_ds = df_filtrado[df_filtrado["cargo"] == "Data Scientist"]
    
    if not df_ds.empty:
        media_ds_pais = df_ds.groupby("residencia_iso3")["usd"].mean().reset_index()
        fig_paises = px.choropleth(
            media_ds_pais,
            locations="residencia_iso3",
            color="usd",
            title="Salário Médio: Data Scientist por País",
            labels={"usd": "Média (USD)"},
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_paises, use_container_width=True)
    else:
        st.info("ℹ️ Selecione filtros que incluam 'Data Scientist' para ver o mapa mundial.")

# --- Tabela ---
st.subheader("Explore os Dados")
st.dataframe(df_filtrado, use_container_width=True)
    
