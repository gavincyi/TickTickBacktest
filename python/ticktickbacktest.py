from config_manager import ConfigManager
from pipe_factory import MysqlPipeFactory
import logging
import argparse
import sys
import time

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

    # Get data names
    order_book_names = config_man.get_orderbook_data_names()
    trade_names = config_man.get_trade_data_names()
    logger.info('Order book names = \n%s' % order_book_names)
    logger.info('Trade names = \n%s' % trade_names)

    # Connect to database
    logger.info('Connecting to database...')
    pipe_factory = MysqlPipeFactory(logger=logger, host=host, port=port, user=username, pwd=pwd, schema=schema)
    db_client = pipe_factory.create()
    if db_client.connect(host=host, port=port, user=username, pwd=pwd, schema=schema):
        logger.info('Database is successful to connect.')

    row = db_client.select(table=order_book_names[0][0],isFetchAll=False)
    logger.info(row)
    row = db_client.fetchone()
    logger.info(row)
    db_client.close()




