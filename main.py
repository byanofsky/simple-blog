import os
import jinja2
import webapp2
import validate
import auth
# from google.appengine.ext import ndb
from datacls import *

# Jinja templating setup
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True,
)

class Handler(webapp2.RequestHandler):
    # TODO: can we have a config file for this?
    site_title = "Simple Blog"

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(
            template,
            page_title=self.get_page_title(),
            seo_title=self.get_seo_title(),
            **kw
        ))

    def get_seo_title(self):
        if hasattr(self, 'page_title') and self.page_title:
            return self.page_title + " - " + self.site_title
        else:
            return self.site_title

    def get_page_title(self):
        if hasattr(self, 'page_title') and self.page_title:
            return self.page_title
        else:
            return self.site_title

    def get_url(self, name):
        return webapp2.uri_for(name)

    def get_user(self):
        # if user cookie, return user id
        pass

    def intialize(self, request, response):
        super().initialize(request, response)

class FrontPageHandler(Handler):
    def get(self):
        posts = Post.query().order(-Post.created).fetch_page(10)
        self.render('frontpage.html', posts=posts)

class SignUpHandler(Handler):
    page_title = 'Signup'

    def get(self):
        self.render('signup.html')

    def post(self):
        email = self.request.get('email')
        pw = self.request.get('password')
        verify = self.request.get('verify')
        displayname = self.request.get('displayname')

        # Validate signup
        errors = validate.signup_errors(email, pw, verify)

        # Check if user exists
        # TODO: can move to validate signup errors
        if User.exists(email):
            errors['user_exists'] = ('There is already a user registered ' +
                                     'with this email.')

        if errors:
            self.render(
                'signup.html',
                email=email,
                displayname=displayname,
                errors=errors)
        else:
            u_key = User.create(email, pw, displayname)
            # TODO: can we move cooki creation to User model class?
            u_cookie = auth.make_secure_val(str(u_key.id()))
            self.response.set_cookie('user_id', u_cookie)
            self.redirect(self.get_url('welcome'))

class WelcomeHandler(Handler):
    def get(self):
        u_cookie = self.request.cookies.get('user_id')
        u_id = auth.check_secure_val(u_cookie)
        displayname = User.get_display_name(u_id)
        self.render('welcome.html', displayname=displayname)

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=FrontPageHandler, name='frontpage'),
    webapp2.Route('/signup', handler=SignUpHandler, name='signup'),
    webapp2.Route('/welcome', handler=WelcomeHandler, name='welcome'),
    # webapp2.Route('/login', handler=LoginHandler, name='login'),
    # webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
    # webapp2.Route('/newpost', handler=NewPostHandler, name='newpost'),
    # webapp2.Route('/<post_id:[0-9]+>', handler=SinglePostHandler, name='singlepost')
], debug=True)
