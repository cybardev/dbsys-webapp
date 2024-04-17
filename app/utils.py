"""
Utility functions
"""

import os

import psycopg

from app.app import app_factory


def render():
    DB_URL = os.environ["DB_URL"]

    # create DB tables if they don't exist
    with psycopg.connect(DB_URL) as db:
        with db.cursor() as cursor:
            for fname in ("parts_table", "make_tables"):
                with open(f"./dbutils/sql/{fname}.sql") as file:
                    cursor.execute(file.read())

    return app_factory(DB_URL)


def sanitize_input(s: str) -> str:
    """Sanitize SQL query string

    Args:
        s (str): query string to sanitize

    Returns:
        str: sanitized query string
    """
    return s.replace(";", "")
