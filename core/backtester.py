from core.execution import ExecutionHandler
from core.portfolio import Portfolio

class Backtester:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy
        self.execution = ExecutionHandler()
        self.portfolio = Portfolio()

    def run(self):
        signals = self.strategy.generate_signals(self.data)

        for date, row in self.data.iterrows():
            price = row['Close']
            spread = (row.get('Spread', 3)) * 0.00001 # fallback to 0.0002 if no column
            signal = signals.loc[date, 'signal']

            order = self.execution.execute_order(signal, price, spread)

            if order:
                self.portfolio.enter_trade(
                    signal=signal,
                    fill_price=order['fill_price'],
                    commission=order['commission'],
                    date=date
                )

            self.portfolio.update(date, price)

    def report(self):
        equity = [eq for _, eq in self.portfolio.equity_curve]
        final = equity[-1] if equity else 0
        print(f"Final Equity: {final:.2f}")
        print(f"Number of Trades: {len(self.portfolio.trade_log)}")

