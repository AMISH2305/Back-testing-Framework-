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
            unrealized = (price - self.entry_price) * self.position * self.active_lot_size
            self.equity = self.cash + unrealized

            # Check SL or TP
            if self.position == 1:  # Long
                if price <= self.stop_loss or price >= self.take_profit:
                    self._close_trade(price, date)
            elif self.position == -1:  # Short
                if price >= self.stop_loss or price <= self.take_profit:
                    self._close_trade(price, date)
        else:
            self.equity = self.cash

        self.equity_curve.append((date, self.equity))

    def _close_trade(self, price, date):
        pnl = (price - self.entry_price) * self.position * self.active_lot_size
        self.cash += pnl
        self.cash -= 4.0  # Fixed exit commission
        self.trade_log.append({
            "action": "EXIT",
            "price": price,
            "pnl": pnl,
            "commission": 4.0,
            "date": date
        })
        self.position = 0
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.active_lot_size = self.lot_size


    def enter_trade(self, signal, fill_price, commission, date, sl=None, tp=None, lot_size=None):
        if self.position == 0 and signal != 0:
            self.position = signal
            self.entry_price = fill_price
            self.stop_loss = sl
            self.take_profit = tp
            self.cash -= commission
            self.active_lot_size = lot_size if lot_size else self.lot_size
            self.trade_log.append({
                "action": "ENTRY",
                "price": fill_price,
                "side": "BUY" if signal == 1 else "SELL",
                "commission": commission,
                "date": date,
                "sl": sl,
                "tp": tp,
                "lot_size": self.active_lot_size
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
