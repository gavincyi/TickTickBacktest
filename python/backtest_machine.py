from pipe_factory import MysqlPipeFactory
from datetime import datetime


class BacktestMachine:
    """
    Backtesting machine
    """

    class UpdateType:
        """
        Update type
        """
        ERROR = -1
        NONE = 1
        DEPTH = 1
        TRADES = 2

    def __init__(self, exchanges={}, logger=None):
        """
        Constructor
        :param exchanges: Exchange dictionary
        """
        self.pipe = None
        self.logger = logger
        self.exchanges = exchanges
        self.strategies = []
        self.open_orders = []
        self.settled_orders = []
        assert self.logger is not None, "Logger cannot be none."

    def prepare_mysql_pipe(self, data_list, logger, host='', port=3306, user='', pwd='', schema=''):
        """
        Prepare MySQL pipe
        :param data_list: Data list
        :param logger: Logger
        :param host: Host
        :param port: Port, defaulted as 3306
        :param user: User names
        :param pwd: Password
        :param schema: Schema
        """
        logger.info('Connecting to database...')
        self.pipe = MysqlPipeFactory(logger=logger, host=host, port=port, user=user, pwd=pwd, schema=schema)
        for data in data_list:
            self.pipe.prepare(data)

    def register_strategy(self, strategy):
        """
        Register strategy
        :param strategy: Strategy
        :return:
        """
        self.strategies.append(strategy)

    def run(self):
        is_continue = True
        while is_continue:
            is_continue, exchange, instmt, update_type = self.__update_next()
            if exchange is None:
                break
            else:
                # Open order first
                for strategy in self.strategies:
                    order = strategy.open_order(exchanges=self.exchanges,
                                                exchange=exchange,
                                                instmt=instmt,
                                                update_type=update_type,
                                                logger=self.logger)
                    if order is not None:
                        self.open_orders.append(order)

                # Close order
                for order in self.open_orders[:]:
                    close_order = order.close()
                    if close_order is not None:
                        self.settled_orders.append(close_order)
                        self.open_orders.remove(order)

        self.logger.info('No more data can be extracted. The run has been finished.')
        for strategy in self.strategies:
            strategy.summary(exchanges=self.exchanges)

    def close(self):
        self.pipe.close()

    def __update_next(self):
        """
        Update the next data row from the pipe
        :return: Exchange name, instrument and the update type. If there is no further update, all return
                 elements are none.
        """
        # Pop the next data row
        is_continue, key, row = self.pipe.pop_next()
        if key is None or row is None:
            return False, None, None, None

        # Get the data info
        assert key in self.pipe.pipes.keys(), "Key (%s) is not in the pipe list" % key
        data_info = self.pipe.pipes[key].data_info
        # Get the exchange name
        assert data_info.exchange in self.exchanges.keys(), "Exchange (%s) is not in the exchange list" % data_info.exchange
        exchange = self.exchanges[data_info.exchange]
        # Get the instrument
        assert data_info.product in exchange.instmts.keys(), "Product (%s) is not in the instrument list" % data_info.product
        instmt = exchange.instmts[data_info.product]

        # Parse the date time
        assert 'date_time' in row.keys(), "Field date_time cannot be found."
        row['date_time'] = datetime.strptime(row['date_time'], data_info.datetime_format)

        # Update
        update_type = BacktestMachine.UpdateType.ERROR
        if data_info.type == 'depth':
            # Update the l2 depth
            update_type = BacktestMachine.UpdateType.DEPTH
            instmt.update_depth(row)
        elif data_info.type == 'trades':
            # Update the last trade
            update_type = BacktestMachine.UpdateType.TRADES
            instmt.update_trade(row)

        return is_continue, exchange, instmt, update_type
