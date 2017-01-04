try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import ast
import os

class ConfigManager:
    """
    Configuration Manager
    """
    class ConfigDataBlock:
        """
        Data block element
        """
        def __init__(self, data):
            self.name = data['name']
            self.table = data['table']
            self.exchange = data['exchange']
            self.product = data['product']
            self.date = data['date']
            self.type = data['type']
            self.datetime_field = data['datetime_field']
            self.datetime_format = data['datetime_format']
            self.settings = data

    class ConfigExchangeBlock:
        """
        Exchange block element
        """
        def __init__(self, data):
            self.name = data['name']
            self.products = data['products']


    class ConfigDataBlockList(list):
        def __init__(self, data_list):
            list.__init__(self)
            for data in data_list:
                self.append(ConfigManager.ConfigDataBlock(data))

    """
    Configuration manager
    """
    def __init__(self, config_path):
        """
        Constructor
        """
        self.__config = ConfigParser.RawConfigParser()
        self.__config.read(os.path.abspath(config_path))
        self.__mysqldb_section_name = 'Mysqldb'
        self.__data_section_name = 'Data'
        self.__exchange_section_name = 'Exchange'

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

    def get_data_names(self):
        return [e[0] for e in self.__config.items(self.__data_section_name)]

    def get_exchange_names(self):
        return [e[0] for e in self.__config.items(self.__exchange_section_name)]

    def get_data(self, name):
        """
        Get orderbook data by name
        :return: Name of the data
        """
        eval_string = self.__config.get(self.__data_section_name, name)
        data = ast.literal_eval(eval_string)
        return ConfigManager.ConfigDataBlockList(data)

    def get_exchange(self, name):
        """
        Get exchange by name
        :return: Name of the exchange`
        """
        eval_string = self.__config.get(self.__exchange_section_name, name)
        data = ast.literal_eval(eval_string)
        return ConfigManager.ConfigExchangeBlock(data)

if __name__ == '__main__':
    config = ConfigManager('config.ini')
    print(config.get_data('Data20161123'))
    print(config.get_exchange_names())
