import os

import webapp2
import jinja2

import validate
import auth
from models.post import Post
from models.comment import Comment
from models.user import User
from google.appengine.ext import ndb
from settings import ROOT_DIR

# Jinja templating setup
# Gets ROOT_DIR from settings
# TODO: is there a better way to handle this?
template_dir = os.path.join(ROOT_DIR, 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True,
)
# Pass uri_for to jinja template to allow template to create uris
jinja_env.globals['uri_for'] = webapp2.uri_for


# TODO: can we move these classes to their own files and not reimport?
class BaseHandler(webapp2.RequestHandler):
    # TODO: check these funcs
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
