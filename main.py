import yfinance as yf
import json
import os

class PortfolioManager:
    """Gerencia a lógica de negócios da carteira de investimentos."""
    
    def __init__(self, database_path='carteira.json'):
        self.database_path = database_path
        self.carteira = self._carregar_dados()

    def _carregar_dados(self):
        if os.path.exists(self.database_path):
            with open(self.database_path, 'r') as f:
                return json.load(f)
        return {}

    def salvar_dados(self):
        with open(self.database_path, 'w') as f:
            json.dump(self.carteira, f, indent=4)

    def registrar_operacao(self, ticker, quantidade, preco_unitario, tipo='compra'):
        """Calcula o Preço Médio e atualiza a quantidade."""
        ticker = ticker.upper()
        if ticker not in self.carteira:
            self.carteira[ticker] = {"quantidade": 0, "preco_medio": 0.0, "alerta_compra": None}

        info = self.carteira[ticker]
        
        if tipo == 'compra':
            custo_total_novo = quantidade * preco_unitario
            custo_total_antigo = info['quantidade'] * info['preco_medio']
            
            info['quantidade'] += quantidade
            info['preco_medio'] = (custo_total_antigo + custo_total_novo) / info['quantidade']
        
        elif tipo == 'venda':
            if quantidade <= info['quantidade']:
                info['quantidade'] -= quantidade
            else:
                print(f"Erro: Saldo insuficiente de {ticker}.")
        
        self.salvar_dados()

    def definir_alerta(self, ticker, preco_alvo):
        ticker = ticker.upper()
        if ticker in self.carteira:
            self.carteira[ticker]['alerta_compra'] = preco_alvo
            self.salvar_dados()

    def gerar_relatorio(self):
        print(f"\n{'ATIVO':<10} | {'QTD':<6} | {'P. MÉDIO':<10} | {'ATUAL':<10} | {'STATUS'}")
        print("-" * 60)
        
        for ticker, dados in self.carteira.items():
            if dados['quantidade'] <= 0: continue
            
            # Busca preço em tempo real
            asset = yf.Ticker(f"{ticker}.SA")
            preco_atual = asset.history(period="1d")['Close'].iloc[-1]
            
            lucro = "🟢" if preco_atual > dados['preco_medio'] else "🔴"
            alerta = ""
            if dados['alerta_compra'] and preco_atual <= dados['alerta_compra']:
                alerta = f" 🔔 OPORTUNIDADE (Abaixo de R${dados['alerta_compra']})"

            print(f"{ticker:<10} | {dados['quantidade']:<6} | R${dados['preco_medio']:>8.2f} | R${preco_atual:>8.2f} | {lucro}{alerta}")

# --- INTERFACE DO USUÁRIO (SIMULANDO O APP DA CORRETORA) ---
def menu():
    manager = PortfolioManager()
    
    while True:
        print("\n--- FINTECH CORE SYSTEM ---")
        print("1. Registrar Compra/Venda")
        print("2. Ver Patrimônio e Alertas")
        print("3. Definir Alerta de Preço")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            t = input("Ticker (ex: VALE3): ")
            q = int(input("Quantidade: "))
            p = float(input("Preço Unitário: "))
            tipo = input("Tipo (compra/venda): ").lower()
            manager.registrar_operacao(t, q, p, tipo)
        elif opcao == '2':
            manager.gerar_relatorio()
        elif opcao == '3':
            t = input("Ticker para alerta: ")
            p = float(input("Preço alvo de compra: "))
            manager.definir_alerta(t, p)
        elif opcao == '4':
            break

if __name__ == "__main__":
    menu()