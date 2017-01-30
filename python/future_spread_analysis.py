from strategy import Strategy
from backtest_machine import BacktestMachine
import pandas as pd
from datetime import datetime

class FutureSpreadAnalysis(Strategy):
    """
    Future spread analysis
    """
    def __init__(self, logger):
        Strategy.__init__(self, logger)
        self.spreads = []

    def open_order(self, **kwargs):
        """
        Open order
        """
        exchanges = kwargs['exchanges']
        exchange = kwargs['exchange']
        instmt = kwargs['instmt']
        update_type = kwargs['update_type']
        logger = kwargs['logger']

        if exchange.name != 'BitMEX' or \
            'XBTUSD' not in exchange.instmts.keys() or \
            'XBTUSD_FUT' not in exchange.instmts.keys():
            return None

        swap_instmt = exchange.instmts['XBTUSD']
        fut_instmt = exchange.instmts['XBTUSD_FUT']

        if update_type == BacktestMachine.UpdateType.TRADES:
            if swap_instmt.last_trade is not None and \
                fut_instmt.last_trade is not None and \
                swap_instmt.last_trade.trade_price > 0 and \
                fut_instmt.last_trade.trade_price > 0 :
                self.spreads.append([swap_instmt.last_trade.date_time.strftime("%Y%m%d %H:%M:%S.%f"),
                                     fut_instmt.last_trade.date_time.strftime("%Y%m%d %H:%M:%S.%f"),
                                     float(swap_instmt.last_trade.trade_price),
                                     float(fut_instmt.last_trade.trade_price)])

        return None

    def summary(self, **kwargs):
        exchange = kwargs['exchanges']['BitMEX']
        arbitrary_info = next(iter(exchange.instmts.values())).l2_depth
        df = pd.DataFrame(self.spreads)
        df.to_csv("result\\future_spread_%s.csv" % arbitrary_info.date_time.strftime("%Y%m%d"),
                  index=False, header=True)


