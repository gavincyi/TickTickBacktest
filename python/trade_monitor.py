from strategy import Strategy
from backtest_machine import BacktestMachine
import datetime
import matplotlib.pyplot as plt
import numpy

class TradeMonitor(Strategy):
    """
    Trade monitor
    Monitor any abnormal of trades
    """
    def __init__(self, logger):
        Strategy.__init__(self, logger)
        self.hour_volume = {}
        self.graph = None
        self.graph_show_index = 0

    def open_order(self, **kwargs):
        """
        Open order
        :param kwargs: Named arguments
        :return: None if no order is opened; Otherwise an order object is returned.
        """
        exchange = kwargs['exchange']
        instmt = kwargs['instmt']
        update_type = kwargs['update_type']
        logger = kwargs['logger']

        if update_type == BacktestMachine.UpdateType.TRADES: # Trade update
            # Update trade info
            self.update_trade_info(instmt.last_trade)

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

    def update_trade_info(self, trade):
        # Update hour volume
        if trade.date_time.hour not in self.hour_volume.keys():
            self.hour_volume[trade.date_time.hour] = trade.trade_volume
        else:
            self.hour_volume[trade.date_time.hour] += trade.trade_volume

        if self.graph is None:
            self.graph, = plt.plot([trade.date_time], [trade.trade_price])
            plt.xlim([trade.date_time, trade.date_time + datetime.timedelta(days=1)])
            plt.gcf().autofmt_xdate()
            plt.draw()
            plt.pause(1)
        elif self.graph_show_index % 100 == 0:
            self.logger.info('Plot now.')
            self.graph.set_xdata(numpy.append(self.graph.get_xdata(), trade.date_time))
            self.graph.set_ydata(numpy.append(self.graph.get_ydata(), trade.trade_price))
            plt.draw()
            plt.pause(1)

        self.graph_show_index += 1

    def summary(self):
        """
        Summary
        Print out the statistical summary after all data are backtested.
        """
        self.logger.info('Hour volume:\n%s', '\n'.join(['%s,%s' % (key, value)for key, value in self.hour_volume.items()]))
        plt.show()
