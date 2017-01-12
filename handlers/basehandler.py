import os

import webapp2
import jinja2

# TODO: is there a better way to import root directory?
from config import app_config

# Jinja templating setup
# TODO: Should this be moved to its own file?
template_dir = os.path.join(app_config['root_dir'], 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True,
)
# Pass uri_for to jinja template to allow template to create uris
jinja_env.globals['uri_for'] = webapp2.uri_for


class BaseHandler(webapp2.RequestHandler):
    # Helper to condense response.out.write
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    # Helper for rendering jinja templates
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    # Helper to combine jinja render and write
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
