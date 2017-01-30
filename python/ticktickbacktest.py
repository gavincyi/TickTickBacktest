from config_manager import ConfigManager
from exchange import Exchange
from backtest_machine import BacktestMachine
from trade_monitor import TradeMonitor
from future_spread_analysis import FutureSpreadAnalysis
import logging
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for backtesting tick data')
    parser.add_argument('-config', action='store', help='Configuration file.', default='config.ini')
    args = parser.parse_args()

    # Setup config
    config_man = ConfigManager(args.config)

    if not config_man.is_mysqldb():
        print('Currently only support getting data from MySQLDB.\n' + \
              'Please specify the seciton [Mysqldb] in the configuration file')
        parser.print_help()
        sys.exit(1)
    elif not config_man.is_data():
        print('No data section in configuration file.\n' + \
              'Please specify the seciton [Data] in the configuration file')
        parser.print_help()
        sys.exit(1)

    # Setup logger
    logger = logging.getLogger('ticktickbacktest')
    logger.setLevel(logging.ERROR)
    logger.setLevel(logging.INFO)
    slogger = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s \n%(message)s\n')
    slogger.setFormatter(formatter)
    logger.addHandler(slogger)

    # Get mysql parameters
    host, port, username, pwd, schema = config_man.get_mysqldb_setup()
    logger.info('Host = %s' % host)
    logger.info('Username = %s' % username)
    logger.info('Schema = %s' % schema)

    # Get exchange names
    exchanges = {}
    exchange_names = config_man.get_exchange_names()
    for exchange_name in exchange_names:
        exchange_info = config_man.get_exchange(exchange_name)
        exchanges[exchange_info.name] = Exchange(exchange_info)

    data_names = config_man.get_data_names()

    for data_name in data_names:
        # Prepare backtest machine
        backtest_machine = BacktestMachine(exchanges=exchanges, logger=logger)
        # Register strategies
        # backtest_machine.register_strategy(TradeMonitor(logger))
        backtest_machine.register_strategy(FutureSpreadAnalysis(logger))

        # Prepare the pipe
        backtest_machine.prepare_mysql_pipe(data_list=config_man.get_data(data_name),
                                            logger=logger,
                                            host=host,
                                            user=username,
                                            pwd=pwd,
                                            schema=schema)
        # Start running
        backtest_machine.run()
        # Close all the pipes
        backtest_machine.close()
