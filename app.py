import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from core import FinanceEngine

st.set_page_config(page_title="FinADS Pro", layout="wide")
engine = FinanceEngine()

st.sidebar.header("Nova Operação")
with st.sidebar.form("trade_form"):
    ticker = st.text_input("Ticker (ex: PETR4)")
    cat = st.selectbox("Categoria", ["Ações", "FIIs", "Fiagros"])
    op = st.radio("Tipo", ["Compra", "Venda"])
    qty = st.number_input("Qtd", min_value=1)
    prc = st.number_input("Preço", min_value=0.01)
    
    if st.form_submit_button("Registrar"):
        try:
            engine.save_operation(ticker, qty, prc, cat, op)
            st.rerun()
        except Exception as e:
            st.error(str(e))

st.title("📊 Meu Portfólio Financeiro")

portfolio = engine.get_data()
if portfolio:
    rows = []
    for sym, info in portfolio.items():
        # Busca cotação atual
        try:
            price_now = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]
        except:
            price_now = info['avg_price']
            
        rows.append({
            "Ativo": sym.replace(".SA", ""),
            "Qtd": info['qty'],
            "P. Médio": round(info['avg_price'], 2),
            "Atual": round(price_now, 2),
            "Total": round(info['qty'] * price_now, 2)
        })
    
    df = pd.DataFrame(rows)
    
    col1, col2 = st.columns([2, 1])
    col1.dataframe(df, use_container_width=True)
    col2.plotly_chart(px.pie(df, values='Total', names='Ativo', title="Alocação"), use_container_width=True)
else:
    st.info("Nenhum ativo cadastrado.")