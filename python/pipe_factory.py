from mysql_client import MysqlClient

class PipeFactory:
    def __init__(self):
        """
        Constructor
        """
        pass

    def create(self):
        """
        Create
        :return: Created object
        """
        return None


class MysqlPipeFactory(PipeFactory):
    """
    Mysql client pipe factory
    """
    def __init__(self, logger=None, host='', port=0, user='', pwd='', schema=''):
        self.logger = logger
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.schema = schema

    def create(self):
        client = MysqlClient(self.logger)
        client.connect(host=self.host, \
                       port=self.port, \
                       user=self.user,
                       pwd=self.pwd,
                       schema=self.schema)
        return client

