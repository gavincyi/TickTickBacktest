from market_data import MarketDataBase, L2Depth, Trade

class Order:
    """
    Order
    """

    def __init__(self, strategy):
        self.side = MarketDataBase.Side.NONE
        self.open_price = 0.0
        self.open_volume = 0.0
        self.close_price = 0.0
        self.volume_done = 0.0
        self.strategy = strategy

    def close(self):
        """
        Close the order
        :return: If the order is closed, itself is returned. Otherwise, none object is returned
        """
        return self.strategy.close_order(self)