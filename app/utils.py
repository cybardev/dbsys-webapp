"""
Utility functions
"""

import os

from app.app import app_factory


def render():
    return app_factory(os.environ["DB_URL"])


def sanitize_input(s: str) -> str:
    """Sanitize SQL query string

    Args:
        s (str): query string to sanitize

    Returns:
        str: sanitized query string
    """
    return s.replace(";", "")
