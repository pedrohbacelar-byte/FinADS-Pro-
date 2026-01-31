import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from core import FinanceEngine

st.set_page_config(page_title="FinADS Pro", layout="wide")
engine = FinanceEngine()

with st.sidebar:
    st.header("Nova Operação")
    with st.form("trade", clear_on_submit=True):
        t = st.text_input("Ticker (ex: PETR4)").upper()
        c = st.selectbox("Categoria", ["Ações", "FIIs", "Fiagros"])
        o = st.radio("Tipo", ["Compra", "Venda"])
        q = st.number_input("Qtd", min_value=1)
        p = st.number_input("Preço", min_value=0.01)
        
        if st.form_submit_button("Registrar"):
            try:
                engine.update_asset(t, q, p, c, o)
                st.rerun()
            except Exception as e:
                st.error(str(e))

st.title("🏦 Dashboard de Investimentos")

data = engine.get_portfolio()
if data:
    rows = []
    for sym, info in data.items():
        try:
            # Busca preço real para o gráfico
            curr = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]
        except:
            curr = info['avg_price']
            
        rows.append({
            "Ativo": sym.replace(".SA", ""),
            "Qtd": info['qty'],
            "Preço Médio": round(info['avg_price'], 2),
            "Total Atual": round(info['qty'] * curr, 2)
        })
    
    df = pd.DataFrame(rows)
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.dataframe(df, hide_index=True, use_container_width=True)
    with col2:
        fig = px.pie(df, values='Total Atual', names='Ativo', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Carteira vazia. Adicione ativos para visualizar o gráfico.")