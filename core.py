import json
import os

class FinanceEngine:
    def __init__(self, file_path='data/portfolio.json'):
        self.file_path = file_path
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def get_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def save_operation(self, ticker, qty, price, cat, op_type):
        ticker = ticker.upper().strip()
        symbol = f"{ticker}.SA" if not ticker.endswith(".SA") else ticker
        data = self.get_data()

        if op_type == "Compra":
            if symbol not in data:
                data[symbol] = {"qty": 0, "avg_price": 0.0, "category": cat}
            
            asset = data[symbol]
            total_cost = (asset['qty'] * asset['avg_price']) + (qty * price)
            asset['qty'] += qty
            asset['avg_price'] = total_cost / asset['qty']
        
        elif op_type == "Venda":
            if symbol in data and data[symbol]['qty'] >= qty:
                data[symbol]['qty'] -= qty
                if data[symbol]['qty'] == 0:
                    del data[symbol]
            else:
                raise ValueError("Saldo insuficiente")

        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)