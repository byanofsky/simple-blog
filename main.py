import os
import jinja2
import webapp2
from google.appengine.ext import db

# Jinja templating setup
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True,
)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get_url(self, name):
        return webapp2.uri_for(name)

class FrontPageHandler(Handler):
    def get(self):
        # posts = Post.all().order("-created").run(limit=10)
        # self.render("front.html", posts=posts)
        self.write("hello")

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=FrontPageHandler, name='frontpage'),
    # webapp2.Route('/signup', handler=SignUpHandler, name='signup'),
    # webapp2.Route('/welcome', handler=WelcomeHandler, name='welcome'),
    # webapp2.Route('/login', handler=LoginHandler, name='login'),
    # webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
    # webapp2.Route('/newpost', handler=NewPostHandler, name='newpost'),
    # webapp2.Route('/<post_id:[0-9]+>', handler=SinglePostHandler, name='singlepost')
], debug=True)
