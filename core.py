import json
import os
import yfinance as yf

class PortfolioCore:
    def __init__(self, path='data/portfolio.json'):
        self.path = path
        self._setup()

    def _setup(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump({}, f)

    def load(self):
        with open(self.path, 'r') as f:
            return json.load(f)

    def save_order(self, ticker, qty, price, category, op_type):
        # Validação de Negócio
        if not ticker or qty <= 0:
            raise ValueError("Dados inválidos. Verifique ticker e quantidade.")

        db = self.load()
        symbol = f"{ticker.upper().strip()}.SA" if not ticker.endswith(".SA") else ticker.upper()

        if op_type == "Venda" and (symbol not in db or db[symbol]['qty'] < qty):
            raise ValueError(f"Saldo insuficiente de {symbol}.")

        if symbol not in db:
            # Normalização da categoria para evitar erros de filtro
            db[symbol] = {"qty": 0, "avg_price": 0.0, "cat": category.strip()}

        asset = db[symbol]
        if op_type == "Compra":
            new_total = (asset['qty'] * asset['avg_price']) + (qty * price)
            asset['qty'] += qty
            asset['avg_price'] = new_total / asset['qty']
        else:
            asset['qty'] -= qty

        with open(self.path, 'w') as f:
            json.dump(db, f, indent=4)
            