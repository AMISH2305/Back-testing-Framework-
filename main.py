from core.backtester import Backtester
from strategies.ma_crossover import MACrossoverStrategy
from data.loader import load_price_data

def main():
    data = load_price_data("data/sample_data.csv")
    strategy = MACrossoverStrategy(short_window=50, long_window=200)
    bt = Backtester(data, strategy)
    bt.run()
    bt.report()

if __name__ == "__main__":
    main()
