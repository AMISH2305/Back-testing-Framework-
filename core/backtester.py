# Backtester core module
class Backtester:
    def __init__(self, data, strategy):
        self.data = data
        self.strategy = strategy

    def run(self):
        print("Running backtest...")

    def report(self):
        print("Backtest complete.")
