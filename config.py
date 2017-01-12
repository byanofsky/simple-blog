import os
# This is the place your app's configuration is
# specified e.g.
#   Third party api keys/secrets
app_config = {
    'API_KEY': 'SOME API KEY.....',
    'debug': True,
    # TODO: use in basehandler. Is there a better way?
    'root_dir': os.path.dirname(os.path.abspath(__file__))
}
