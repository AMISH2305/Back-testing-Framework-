import pandas as pd

class FVGStrategy:
    def __init__(self, gap_window=3, direction="both"):
        self.gap_window = gap_window
        self.direction = direction

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0

        for i in range(self.gap_window, len(data)):
            prev_low = data['Low'].iloc[i - 2]
            prev_high = data['High'].iloc[i - 2]
            curr_low = data['Low'].iloc[i]
            curr_high = data['High'].iloc[i]

            # Bullish FVG: Previous high < current low
            if self.direction in ["buy", "both"] and prev_high < curr_low:
                # Price enters the gap from above = buy setup
                if data['Low'].iloc[i] <= prev_high:
                    signals.iloc[i, signals.columns.get_loc("signal")] = 1

            # Bearish FVG: Previous low > current high
            if self.direction in ["sell", "both"] and prev_low > curr_high:
                # Price enters the gap from below = sell setup
                if data['High'].iloc[i] >= prev_low:
                    signals.iloc[i, signals.columns.get_loc("signal")] = -1

        return signals
