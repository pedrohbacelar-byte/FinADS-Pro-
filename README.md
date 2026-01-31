# 🏦 FinADS-Core: Gestão Inteligente de Ativos

Sistema de monitoramento de carteira de investimentos desenvolvido para aplicar conceitos de **Análise e Desenvolvimento de Sistemas (ADS)**. O projeto integra dados em tempo real da B3 com uma interface analítica moderna.

## 🚀 Funcionalidades
- **Gestão Multiclasse**: Separação automática entre Ações e FIIs/Fiagros.
- **Cálculo de Preço Médio**: Algoritmo que processa novas compras e atualiza o custo médio ponderado.
- **Integração em Tempo Real**: Consumo de cotações via API `yfinance`.
- **Visualização de Dados**: Gráficos dinâmicos de alocação de ativos e tabelas com formatação condicional (Lucro/Prejuízo).

## 🛠️ Tecnologias e Conceitos de ADS
- **Python**: Linguagem base.
- **Streamlit**: Framework para interface web.
- **Pandas**: Manipulação de DataFrames.
- **Plotly**: Visualizações gráficas interativas.
- **Modularização**: Separação entre lógica de negócio (`core.py`) e interface (`app.py`).

## 📁 Como rodar o projeto
1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`.
3. Ative o venv: `.\venv\Scripts\activate`.
4. Instale as dependências: `pip install -r requirements.txt`.
5. Execute: `streamlit run app.py`.

---
**Contato e Portfólio:**
- 🎓 Graduado em ADS 
- 📧 pedrohbacelar@gmail.com
- 🔗 www.linkedin.com/in/pedrohbacelar