import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_equity_curve(equity_curve):
    df = pd.DataFrame(equity_curve, columns=["Date", "Equity"])
    df.set_index("Date", inplace=True)

    plt.figure(figsize=(10, 5))
    plt.plot(df, label="Equity Curve", color='blue')
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Equity ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def calculate_performance_metrics(equity_curve):
    df = pd.DataFrame(equity_curve, columns=["Date", "Equity"])
    df.set_index("Date", inplace=True)
    returns = df['Equity'].pct_change().dropna()

    sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
    total_return = df['Equity'].iloc[-1] / df['Equity'].iloc[0] - 1
    max_drawdown = (df['Equity'].cummax() - df['Equity']).max()
    win_rate = None  # We'll add this later from trade log if needed

    return {
        "Total Return (%)": total_return * 100,
        "Sharpe Ratio": sharpe,
        "Max Drawdown ($)": max_drawdown
    }
