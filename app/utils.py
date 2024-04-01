"""
Utility functions
"""


def sanitize_input(s: str) -> str:
    """Sanitize SQL query string

    Args:
        s (str): query string to sanitize

    Returns:
        str: sanitized query string
    """
    return s.replace(";", "")
