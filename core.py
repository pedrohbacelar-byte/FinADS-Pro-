import json
import os

class FinanceEngine:
    def __init__(self, file_path='data/portfolio.json'):
        self.file_path = file_path
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(self.file_path):
            self._write({})

    def _write(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def get_portfolio(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def update_asset(self, ticker, qty, price, category, op_type):
        ticker = ticker.upper().strip()
        symbol = f"{ticker}.SA" if not ticker.endswith(".SA") else ticker
        data = self.get_portfolio()

        if op_type == "Compra":
            if symbol not in data:
                data[symbol] = {"qty": 0, "avg_price": 0.0, "category": category}
            
            asset = data[symbol]
            new_qty = asset['qty'] + qty
            asset['avg_price'] = ((asset['qty'] * asset['avg_price']) + (qty * price)) / new_qty
            asset['qty'] = new_qty
        
        elif op_type == "Venda":
            if symbol in data and data[symbol]['qty'] >= qty:
                data[symbol]['qty'] -= qty
                if data[symbol]['qty'] <= 0:
                    del data[symbol]
            else:
                raise ValueError("Saldo insuficiente")

        self._write(data)