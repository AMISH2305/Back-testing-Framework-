import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

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

def export_trade_log_to_csv(trade_log, filename="trade_log.csv"):
    df = pd.DataFrame(trade_log)
    df.to_csv(filename, index=False)
    print(f"✅ Trade log saved to: {filename}")

def analyze_trades(trade_log):
    trade_df = pd.DataFrame(trade_log)
    trade_df = trade_df[trade_df["action"] == "EXIT"]

    if trade_df.empty:
        return {
            "Total Trades": 0,
            "Win Rate (%)": 0.0,
            "Average PnL ($)": 0.0
        }

    total_trades = len(trade_df)
    wins = trade_df[trade_df["pnl"] > 0]
    win_rate = len(wins) / total_trades * 100
    avg_pnl = trade_df["pnl"].mean()

    return {
        "Total Trades": total_trades,
        "Win Rate (%)": win_rate,
        "Average PnL ($)": avg_pnl
    }

def drawdown_heatmap(equity_curve):
    df = pd.DataFrame(equity_curve, columns=["Date", "Equity"])
    df.set_index("Date", inplace=True)
    df["Roll_Max"] = df["Equity"].cummax()
    df["Drawdown"] = df["Roll_Max"] - df["Equity"]

    # Pivot into year/month heatmap
    df["Year"] = df.index.year
    df["Month"] = df.index.month
    pivot = df.pivot_table(index="Month", columns="Year", values="Drawdown", aggfunc="max")

    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, cmap="Reds", annot=True, fmt=".0f", cbar_kws={'label': 'Max Drawdown ($)'})
    plt.title("Monthly Max Drawdown Heatmap")
    plt.xlabel("Year")
    plt.ylabel("Month")
    plt.tight_layout()
    plt.show()
