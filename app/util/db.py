from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from config import db_config


class my_connection(Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cursor(self, cursor=None):
        if cursor:
            return cursor(self)
        self.ping()
        return self.cursorclass(self)


connection = my_connection(**db_config, cursorclass=DictCursor)
