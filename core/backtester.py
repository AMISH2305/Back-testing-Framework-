from core.execution import ExecutionHandler
from core.portfolio import Portfolio
from utils.metrics import plot_equity_curve, calculate_performance_metrics

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
        print("=== Backtest Report ===")
        equity = self.portfolio.equity_curve
        if not equity:
            print("No trades or equity data.")
            return

        metrics = calculate_performance_metrics(equity)
        for k, v in metrics.items():
            print(f"{k}: {v:.2f}")

        plot_equity_curve(equity)

