import webapp2
import os

from routes import route_list
from config import app_config

# TODO: Handling with or without backslash
app = webapp2.WSGIApplication(
    route_list,
    config=app_config,
    debug=app_config.get('debug', False)
)
