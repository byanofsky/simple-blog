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

# TODO: can we move these classes to their own files and not reimport?

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

    # if user cookie, return user id
    # def get_user_id(self):
    #     u_cookie = self.request.cookies.get('user_id')
    #     if u_cookie:
    #         return auth.check_secure_val(u_cookie)
    #     else:
    #         return None

    def get_loggedin_user(self):
        u_id = auth.get_user_cookie_id(self)
        if u_id:
            return User.key_by_id(int(u_id)).get()
        else:
            return None
    #
    # def set_user_cookie(self, user_key):
    #     u_cookie = auth.make_secure_val(str(user_key.id()))
    #     self.response.set_cookie('user_id', u_cookie)
    #
    # def clear_user_cookie(self):
    #     self.response.set_cookie('user_id', None)

    def initialize(self, request, response):
        super(Handler, self).initialize(request, response)
        self.u = self.get_loggedin_user()
        if not self.u:
            auth.clear_user_cookie(self)

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

        if errors:
            self.render(
                'signup.html',
                email=email,
                displayname=displayname,
                errors=errors)
        else:
            u_key = User.create(email, pw, displayname)
            auth.set_user_cookie(self, u_key)
            self.redirect(self.get_url('welcome'))

class WelcomeHandler(Handler):
    page_title = 'Welcome'

    def get(self):
        if not self.u:
            self.redirect(self.get_url('signup'))
        else:
            displayname = self.u.displayname
            self.render('welcome.html', displayname=displayname)

class LoginHandler(Handler):
    page_title = 'Login'

    def get(self):
        self.render('login.html')

    def post(self):
        email = self.request.get('email')
        pw = self.request.get('password')

        errors = validate.login_errors(email, pw)

        if errors:
            self.render('login.html', email=email, errors=errors)
        else:
            # TODO: making 2 calls to db. 1 here and 2 in
            u_key = User.get_by_email(email).key
            auth.set_user_cookie(self, u_key)
            self.redirect(self.get_url('welcome'))

class LogoutHandler(Handler):
    def get(self):
        if self.u:
            auth.clear_user_cookie(self)
        self.redirect(self.get_url('login'))

class NewPostHandler(Handler):
    page_title = 'New Post'

    def get(self):
        # TODO: move redirect to intialize?
        if not self.u:
            self.redirect(self.get_url('login'))
        else:
            self.render('newpost.html')

    def post(self):
        # TODO: move redirect to initialize?
        if not self.u:
            self.redirect(self.get_url('login'))
        else:
            title = self.request.get('title')
            body = self.request.get('body')

            errors = validate.newpost_errors(title, body)

            if errors:
                self.render('newpost.html', title=title, body=body, errors=errors)
            else:
                p_key = Post.create(title, body, self.u.key)
                self.write('success')

class SinglePostHandler(Handler):
    def get(self, post_id):
        p = Post.get_by_id(int(post_id))


app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=FrontPageHandler, name='frontpage'),
    webapp2.Route('/signup', handler=SignUpHandler, name='signup'),
    webapp2.Route('/welcome', handler=WelcomeHandler, name='welcome'),
    webapp2.Route('/login', handler=LoginHandler, name='login'),
    webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
    webapp2.Route('/newpost', handler=NewPostHandler, name='newpost'),
    webapp2.Route('/<post_id:[0-9]+>', handler=SinglePostHandler, name='singlepost')
], debug=True)
