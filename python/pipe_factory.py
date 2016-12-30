from mysql_client import MysqlClient
import datetime

class PipeStatus:
    def __init__(self, data_info, client=None):
        self.data_info = data_info
        self.client = client
        self.next_cursor = None
        self.curr_cursor = None
        self.is_end = False


class PipeFactory:
    def __init__(self):
        """
        Constructor
        """
        self.pipes = {}

    def prepare(self, table_name):
        """
        Create
        :return: Prepare the pipe
        """
        return None


class MysqlPipeFactory(PipeFactory):
    """
    Mysql client pipe factory
    """
    def __init__(self, logger=None, host='', port=0, user='', pwd='', schema=''):
        PipeFactory.__init__(self)
        self.logger = logger
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.schema = schema

    def prepare(self, data_info):
        if data_info.table not in self.pipes.keys():
            client = MysqlClient(self.logger)
            client.connect(host=self.host, \
                           port=self.port, \
                           user=self.user,
                           pwd=self.pwd,
                           schema=self.schema)
            curr_row = client.select(table=data_info.table, isFetchAll=False)
            next_row = client.fetchone()
            pipe_status = PipeStatus(data_info, client)
            pipe_status.curr_cursor = curr_row
            pipe_status.next_cursor = next_row

            self.pipes[data_info.name] = pipe_status
        else:
            raise Exception("Table name (%s) is prepared before" % data_info.table)

    def pop_next(self):
        min_time = datetime.datetime.now()
        min_args_key = ''

        for key, value in self.pipes.items():
            data_info = value.data_info
            timestamp = datetime.datetime.strptime(value.next_cursor[data_info.datetime_field],
                                                   data_info.datetime_format)
            if timestamp < min_time:
                min_time = timestamp
                min_args_key = key

        min_args = self.pipes[min_args_key]
        min_args.curr_cursor = min_args.next_cursor.copy()
        min_args.next_cursor = min_args.client.fetchone()

        return min_args_key, min_args.curr_cursor

    def close(self):
        for key, value in self.pipes.items():
            value.client.close()



