import streamlit as st

st.set_page_config(page_title="Meu primeiro dashboard", layout="centered")

st.title("Dashboard de Teste 🚀")

st.write("Se você está vendo isso, o deploy funcionou.")

numero = st.slider("Escolha um número", 0, 100, 50)
st.write("Você escolheu:", numero)
Add streamlit_app.py
