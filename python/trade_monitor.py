from strategy import Strategy
from backtest_machine import BacktestMachine
import datetime

class TradeMonitor(Strategy):
    """
    Trade monitor
    Monitor any abnormal of trades
    """
    def __init__(self, logger):
        Strategy.__init__(self, logger)
        self.hour_volume = {}
        self.graph_trade = None
        self.graph_b1 = None
        self.graph_show_index = 0

    def open_order(self, **kwargs):
        """
        Open order
        :param kwargs: Named arguments
        :return: None if no order is opened; Otherwise an order object is returned.
        """
        exchanges = kwargs['exchanges']
        instmt = kwargs['instmt']
        update_type = kwargs['update_type']
        logger = kwargs['logger']

        if update_type == BacktestMachine.UpdateType.TRADES: # Trade update
            # Update trade info
            self.update_trade_info(instmt)

            if instmt.last_trade.trade_price <= instmt.l2_depth.bids[1].price or \
               instmt.last_trade.trade_price >= instmt.l2_depth.asks[1].price:
                logger.info('%s\n%s\n%s\n%s', \
                            instmt.prev_l2_depth.values(), \
                            instmt.l2_depth.values(), \
                            instmt.last_trade.values(), \
                            [e.trade_price for e in instmt.trade_history])
            elif instmt.last_trade.date_time == instmt.l2_depth.date_time and \
                (instmt.last_trade.trade_price <= instmt.l2_depth.bids[0].price or \
                 instmt.last_trade.trade_price >= instmt.l2_depth.asks[0].price):
                logger.info('%s\n%s\n%s\n%s', \
                            instmt.prev_l2_depth.values(), \
                            instmt.l2_depth.values(), \
                            instmt.last_trade.values(), \
                            [e.trade_price for e in instmt.trade_history])
        return None

    def update_trade_info(self, instmt):
        trade = instmt.last_trade
        l2_depth = instmt.l2_depth

        # Update hour volume
        self.hour_volume.setdefault(instmt.name, {}).setdefault(trade.date_time.hour, 0)
        self.hour_volume[instmt.name][trade.date_time.hour] += trade.trade_volume

        # Plot the graph
        if instmt.name == 'XBTUSD':
            if self.graph_show_index % 10 == 0:
                self.graph_trade = self.plot_graph(trade.date_time, trade.trade_price, self.graph_trade)
                # self.graph_b1 = self.plot_graph(trade.date_time, l2_depth.bids[0].price, self.graph_b1)

            self.graph_show_index += 1

    def summary(self):
        """
        Summary
        Print out the statistical summary after all data are backtested.
        """
        self.plot_show()
        for key, value in self.hour_volume.items():
            ret = ""
            for hour, vol in value.items():
                ret += '%d: %.2f\n' % (hour, vol)
            self.logger.info('Summary [%s]:\n%s' % (key, ret))

