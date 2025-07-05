import pandas as pd

class MACrossoverStrategy:
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        signals['short_ma'] = data['Close'].rolling(window=self.short_window).mean()
        signals['long_ma'] = data['Close'].rolling(window=self.long_window).mean()
        signals['signal'][self.short_window:] = \
            (signals['short_ma'][self.short_window:] > signals['long_ma'][self.short_window:]).astype(int)
        return signals
