import json
import os
import yfinance as yf

class FinanceEngine:
    def __init__(self, storage_path='data/portfolio.json'):
        self.storage_path = storage_path
        self._init_storage()

    def _init_storage(self):
        """Cria a pasta e o arquivo json caso não existam."""
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump({}, f)

    def get_portfolio(self):
        with open(self.storage_path, 'r') as f:
            return json.load(f)

    def process_transaction(self, ticker, qty, price, category, operation_type):
        """
        Calcula preço médio em compras e abate quantidade em vendas.
        """
        if qty <= 0 or price <= 0:
            raise ValueError("Quantidade e preço devem ser maiores que zero.")

        data = self.get_portfolio()
        ticker = ticker.upper().strip()
        # Formata para o padrão do Yahoo Finance
        symbol = f"{ticker}.SA" if not ticker.endswith(".SA") else ticker

        if symbol not in data:
            if operation_type == "Venda":
                raise ValueError("Não é possível vender um ativo que não está na carteira.")
            data[symbol] = {"qty": 0, "avg_price": 0.0, "category": category}

        asset = data[symbol]

        if operation_type == "Compra":
            total_invested = (asset['qty'] * asset['avg_price']) + (qty * price)
            asset['qty'] += qty
            asset['avg_price'] = total_invested / asset['qty']
        else:
            if qty > asset['qty']:
                raise ValueError("Quantidade de venda superior ao saldo em carteira.")
            asset['qty'] -= qty

        # Remove o ativo se a quantidade zerar
        if asset['qty'] <= 0:
            del data[symbol]

        self._save(data)

    def _save(self, data):
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=4)