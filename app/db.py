"""
Context manager class for handling datbase connections
"""

import MySQLdb


class Database:
    def __init__(self, hostname, username, password, database) -> None:
        self.__host = hostname
        self.__user = username
        self.__pass = password
        self.__db = database
        self.__conn = None
        self.__cur = None

    @property
    def connection(self):
        return self.__conn

    @property
    def cursor(self):
        return self.__cur

    def __enter__(self):
        self.__conn = MySQLdb.connect(
            host=self.__host, user=self.__user, passwd=self.__pass, db=self.__db
        )
        self.__cur = self.__conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> bool:
        if exc_type is None:
            self.__conn.commit()
        else:
            print(f"Error: {exc_value}")
            self.__conn.rollback()
            return False

        self.__cur.close()
        self.__conn.close()
        return True
