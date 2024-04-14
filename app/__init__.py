# module declaration script

import os

from app.app import app_factory


render = app_factory(
    "localhost",
    os.environ["DB_USER"],
    os.environ["DB_PASS"],
    os.environ["DB_NAME"],
)
