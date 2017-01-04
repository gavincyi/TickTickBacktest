from market_data import L2Depth, Trade
import datetime

class Exchange:
    """
    Exchange
    """
    def __init__(self, exch_config_block):
        self.name = exch_config_block.name
        self.instmts = {}
        for product in exch_config_block.products:
            name = product['name']
            self.instmts[name] = Instrument(name, product)

class Instrument:
    """
    Instrument
    """
    def __init__(self, name, info):
        self.name = name
        self.info = info
        self.prev_l2_depth = L2Depth()
        self.l2_depth = L2Depth()
        self.last_trade = Trade()
        self.trade_history = []
        self.trade_history_max_sec = datetime.timedelta(seconds=60)

    def update_depth(self, row):
        self.prev_l2_depth = self.l2_depth.copy()
        self.l2_depth.update(row)

    def update_trade(self, row):
        self.last_trade.update(row)
        self.trade_history.append(self.last_trade.copy())

        index = -1
        for i in range(len(self.trade_history)-1, 0, -1):
            if self.last_trade.date_time - self.trade_history[i].date_time > self.trade_history_max_sec:
                index = i
                break

        if index > -1:
            del self.trade_history[0:index+1]

