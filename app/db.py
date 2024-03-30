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
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = MySQLdb.connect(
            host=self.__host, user=self.__user, passwd=self.__pass, db=self.__db
        )
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> bool:
        if exc_type is None:
            self.conn.commit()
        else:
            print(f"Error: {exc_value}")
            self.conn.rollback()
            return False

        self.cur.close()
        self.conn.close()
        return True
