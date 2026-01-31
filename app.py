import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from core import PortfolioCore

# Setup de Página
st.set_page_config(page_title="FinADS Hub", layout="wide")
core = PortfolioCore()

st.title("⚖️ FinADS: Gestão de Ativos")

# Sidebar - Registro de Ordens
with st.sidebar:
    st.header("📋 Terminal de Operações")
    with st.form("trade_form", clear_on_submit=True):
        t_input = st.text_input("Ticker").upper()
        # Categorias fixas para garantir o match no banco de dados
        c_input = st.selectbox("Tipo de Ativo", ["Ações", "FIIs/Fiagros"])
        op_input = st.radio("Lado", ["Compra", "Venda"])
        q_input = st.number_input("Quantidade", min_value=0)
        p_input = st.number_input("Preço Unitário", min_value=0.0, format="%.2f")
        
        if st.form_submit_button("Enviar Ordem"):
            try:
                core.save_order(t_input, q_input, p_input, c_input, op_input)
                st.success("Enviado com sucesso!")
                st.rerun() # Atualiza a tela imediatamente
            except ValueError as e:
                st.error(str(e))

# Camada de Dados e Mercado
raw_data = core.load()
if raw_data and any(v['qty'] > 0 for v in raw_data.values()):
    rows = []
    for sym, info in raw_data.items():
        if info['qty'] <= 0: continue
        
        try:
            # Atualização Automática
            price_now = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]
        except:
            price_now = info['avg_price']

        current_market_val = info['qty'] * price_now
        total_cost = info['qty'] * info['avg_price']
        profit_loss = current_market_val - total_cost

        rows.append({
            "Ativo": sym.split(".")[0],
            "Cat": info['cat'],
            "Qtd": info['qty'],
            "Médio": info['avg_price'],
            "Atual": price_now,
            "Patrimônio": current_market_val,
            "Resultado": profit_loss
        })

    df = pd.DataFrame(rows)

    # Painel de Controle (Tabs)
    tab1, tab2, tab3 = st.tabs(["📊 Ações", "🚜 FIIs/Fiagros", "📉 Alocação"])

    def draw_styled_table(data):
        return st.dataframe(
            data.style.applymap(
                lambda x: 'color: #ff4b4b' if x < 0 else 'color: #28a745', 
                subset=['Resultado']
            ).format(precision=2),
            use_container_width=True
        )

    with tab1:
        # Filtro exato por categoria
        df_stocks = df[df['Cat'] == "Ações"]
        if not df_stocks.empty: draw_styled_table(df_stocks)
        else: st.info("Nenhuma Ação na carteira.")

    with tab2:
        # Filtro exato por categoria
        df_reits = df[df['Cat'] == "FIIs/Fiagros"]
        if not df_reits.empty: draw_styled_table(df_reits)
        else: st.info("Nenhum FII/Fiagro na carteira.")

    with tab3:
        # Gráfico de Rosca (Corrigido)
        fig = px.pie(df, values='Patrimônio', names='Ativo', hole=0.5,
                     title="Composição da Carteira", 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Sistema aguardando inserção de dados.")