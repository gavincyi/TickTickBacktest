try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import ast

class ConfigManager:
    """
    Configuration manager
    """
    def __init__(self, config_path):
        """
        Constructor
        """
        self.__config = ConfigParser.ConfigParser()
        self.__config.read(config_path)
        self.__mysqldb_section_name = 'Mysqldb'
        self.__data_section_name = 'Data'

    def is_mysqldb(self):
        """
        Check if section Mysqldb is found
        :return: True if the section is found
        """
        return self.__mysqldb_section_name in self.__config.sections()

    def get_mysqldb_setup(self):
        """
        Get mysqldb setup
        :return: Host (e.g. 127.0.0.1), Port, Username, Password, Schema
        """
        return self.__config.get(self.__mysqldb_section_name, 'Host'), \
               int(self.__config.get(self.__mysqldb_section_name, 'Port')), \
               self.__config.get(self.__mysqldb_section_name, 'Username'), \
               self.__config.get(self.__mysqldb_section_name, 'Password'), \
               self.__config.get(self.__mysqldb_section_name, 'Schema')

    def is_data(self):
        """
        Check if section data is found
        :return: True if the section is found
        """
        return self.__data_section_name in self.__config.sections()

    def get_orderbook_data_names(self):
        """
        Get orderbook data names
        :return: List of names
        """
        return ast.literal_eval(self.__config.get(self.__data_section_name, 'Orderbook'))

    def get_trade_data_names(self):
        """
        Get trades data names
        :return: List of names
        """
        return ast.literal_eval(self.__config.get(self.__data_section_name, 'Trades'))

