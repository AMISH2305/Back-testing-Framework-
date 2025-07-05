from core.execution import ExecutionHandler
from core.portfolio import Portfolio
from utils.metrics import plot_equity_curve, calculate_performance_metrics

class Backtester:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy
        self.execution = ExecutionHandler()
        self.portfolio = Portfolio()
        
    def calculate_position_size(self, stop_distance, risk_percent=0.02):
        risk_amount = self.portfolio.equity * risk_percent
        units = risk_amount / stop_distance
        return min(units, 500000) 

    def run(self):
        signals = self.strategy.generate_signals(self.data)

        for date, row in self.data.iterrows():
            price = row['Close']
            spread = (row.get('Spread', 3)) * 0.00001 # fallback to 0.0002 if no column
            signal = signals.loc[date, 'signal']

            order = self.execution.execute_order(signal, price, spread)

            if order:
                stop_distance = 0.0020  # 20 pips
                take_profit_distance = 0.0040  # 40 pips

                if signal == 1:  # Buy
                    sl = order['fill_price'] - stop_distance
                    tp = order['fill_price'] + take_profit_distance
                elif signal == -1:  # Sell
                    sl = order['fill_price'] + stop_distance
                    tp = order['fill_price'] - take_profit_distance

                lot_size = self.calculate_position_size(stop_distance)

                self.portfolio.enter_trade(
                    signal=signal,
                    fill_price=order['fill_price'],
                    commission=order['commission'],
                    date=date,
                    sl=sl,
                    tp=tp,
                    lot_size=lot_size
                )
                

    def report(self):
        print("=== Backtest Report ===")
        equity = self.portfolio.equity_curve
        trades = self.portfolio.trade_log

        if not equity:
            print("No trades or equity data.")
            return

        # Performance metrics
        metrics = calculate_performance_metrics(equity)
        for k, v in metrics.items():
            print(f"{k}: {v:.2f}")

        # Trade analysis
        trade_stats = analyze_trades(trades)
        for k, v in trade_stats.items():
            print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")

        # Export log
        export_trade_log_to_csv(trades)

        # Plots
        plot_equity_curve(equity)
        drawdown_heatmap(equity)


