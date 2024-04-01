import logging

import MySQLdb


class Database:
    """
    Context manager class for handling database connections
    """

    def __init__(
        self, hostname: str, username: str, password: str, database: str
    ) -> None:
        """Constructor for database context manager

        Args:
            hostname (str): hostname of the database server
            username (str): username for the database server
            password (str): password for the database server
            database (str): name of database to connect to
        """
        self.__host = hostname
        self.__user = username
        self.__pass = password
        self.__db = database
        self.__conn = None
        self.__cur = None

    @property
    def connection(self):
        """Database connection property"""
        return self.__conn

    @property
    def cursor(self):
        """Database cursor property"""
        return self.__cur

    def __enter__(self):
        """Initialize database connection and cursor

        Returns:
            Database: modified context manager instance
        """
        self.__conn = MySQLdb.connect(
            host=self.__host, user=self.__user, passwd=self.__pass, db=self.__db
        )
        logging.info("Database connection established")
        self.__cur = self.__conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> bool:
        """Clean-up and exception handling

        Args:
            exc_type: class of exception (or None)
            exc_value: instance of exception (or None)
            exc_traceback: traceback of exception (or None)

        Returns:
            bool: True if exception has been handled, False if propagated to caller
        """
        try:
            if exc_type is None:
                logging.info("Committing changes to database")
                self.__conn.commit()
            else:
                logging.error(f"Error: {exc_value}")
                self.__conn.rollback()
                return False
        except MySQLdb.Error as e:
            logging.error(f"Error while exiting context manager: {e}")
            return False
        finally:
            logging.info("Closing database connection")
            self.__cur.close()
            self.__conn.close()

        return True
