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
    data_list = config_man.get_data('Data20161123')
    logger.info('Data list = %s' % data_list)

    # Connect to database
    logger.info('Connecting to database...')
    pipe_factory = MysqlPipeFactory(logger=logger, host=host, port=port, user=username, pwd=pwd, schema=schema)
    for data in data_list:
        pipe_factory.prepare(data)

    for i in range(0, 100):
        key, row = pipe_factory.pop_next()
        logger.info('%d: %s - Next = %s' % (i, key, row))

    pipe_factory.close()

