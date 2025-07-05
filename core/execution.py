class ExecutionHandler:
    def __init__(self, commission_per_lot=4.0, lot_size=100000):
        self.commission_per_lot = commission_per_lot
        self.lot_size = lot_size

    def execute_order(self, signal, price, spread):
        """
        Executes a market order with dynamic spread.
        Args:
            signal: 1 for Buy, -1 for Sell, 0 for Hold
            price: mid price (Close price)
            spread: current spread from dataset (in price units)
        Returns:
            dict with fill_price, commission, direction
        """
        if signal == 0:
            return None

        direction = "BUY" if signal == 1 else "SELL"
        
        # Market orders: Buy at ask, Sell at bid
        if direction == "BUY":
            fill_price = price + (spread * 0.00001)
        else:
            fill_price = price - (spread * 0.00001)

        # Commission is fixed per lot
        commission = self.commission_per_lot * (self.lot_size / 100000)

        return {
            "fill_price": fill_price,
            "commission": commission,
            "direction": direction
        }
