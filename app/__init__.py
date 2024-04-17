# module init script

import os

from app.app import app_factory

render = app_factory(os.environ["DB_URL"])
