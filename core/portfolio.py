class Portfolio:
    def __init__(self, initial_cash=10000, lot_size=1000):
        self.cash = initial_cash
        self.equity = initial_cash
        self.lot_size = lot_size
        self.position = 0  # +1 for long, -1 for short, 0 for flat
        self.entry_price = None
        self.trade_log = []
        self.equity_curve = []

    def update(self, date, price):
        if self.position != 0:
            unrealized = (price - self.entry_price) * self.position * self.lot_size
        else:
            unrealized = 0
        self.equity = self.cash + unrealized
        self.equity_curve.append((date, self.equity))

    def enter_trade(self, signal, fill_price, commission, date):
        if self.position == 0 and signal != 0:
            self.position = signal
            self.entry_price = fill_price
            self.cash -= commission
            self.trade_log.append({
                "action": "ENTRY",
                "price": fill_price,
                "side": "BUY" if signal == 1 else "SELL",
                "commission": commission,
                "date": date
            })

         elif self.position != 0 and signal == 0:
            # Exit trade
            pnl = (fill_price - self.entry_price) * self.position * self.lot_size
            self.cash += pnl
            self.cash -= commission  # apply commission on exit
            self.trade_log.append({
                "action": "EXIT",
                "price": fill_price,
                "pnl": pnl,
                "commission": commission,
                "date": date
            })
            self.position = 0
            self.entry_price = None
