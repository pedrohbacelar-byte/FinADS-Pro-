import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from core import FinanceEngine

st.set_page_config(page_title="FinADS Pro", layout="wide")
engine = FinanceEngine()

with st.sidebar:
    st.header("Cadastrar Operação")
    with st.form("trade", clear_on_submit=True):
        t = st.text_input("Ticker (ex: PETR4)").upper()
        c = st.selectbox("Categoria", ["Ações", "FIIs/Fiagros"])
        o = st.radio("Operação", ["Compra", "Venda"])
        q = st.number_input("Quantidade", min_value=1)
        p = st.number_input("Preço Unitário", min_value=0.01)
        
        if st.form_submit_button("Confirmar"):
            try:
                engine.update_asset(t, q, p, c, o)
                st.rerun()
            except Exception as e:
                st.error(str(e))

st.title("🏦 Gestão de Ativos - ADS")

data = engine.get_portfolio()

if data:
    rows = []
    for sym, info in data.items():
        try:
            curr = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]
        except:
            curr = info.get('avg_price', 0)
        
        rows.append({
            "Ativo": sym.replace(".SA", ""),
            "Categoria": info.get('category', 'Ações'),
            "Qtd": info['qty'],
            "P. Médio": round(info['avg_price'], 2),
            "Total": round(info['qty'] * curr, 2)
        })
    
    df = pd.DataFrame(rows)
    tab1, tab2, tab3 = st.tabs(["📊 Geral", "📈 Ações", "🏢 FIIs/Fiagros"])
    
    with tab1:
        st.plotly_chart(px.pie(df, values='Total', names='Ativo', hole=0.3), use_container_width=True)
        st.dataframe(df, hide_index=True, use_container_width=True)

    with tab2:
        df_a = df[df['Categoria'] == 'Ações']
        if not df_a.empty:
            st.dataframe(df_a, hide_index=True, use_container_width=True)
        else:
            st.info("Nenhuma Ação na carteira.")

    with tab3:
        df_f = df[df['Categoria'] == 'FIIs/Fiagros']
        if not df_f.empty:
            st.dataframe(df_f, hide_index=True, use_container_width=True)
        else:
            st.info("Nenhum FII ou Fiagro na carteira.")
else:
    st.warning("O sistema está pronto. Cadastre um ativo no menu lateral para iniciar.")