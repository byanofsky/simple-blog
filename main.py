# TODO: go through imports
import os
import jinja2
import webapp2
import validate
import auth
import yaml
from datacls import *
from google.appengine.datastore.datastore_query import Cursor

# load config settings
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# Jinja templating setup
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True,
)

# TODO: can we move these classes to their own files and not reimport?
class Handler(webapp2.RequestHandler):
    site_title = cfg['site_title']

    # code to simplify jinja
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(
            self.render_str(
                template,
                page_title=self.get_page_title(),
                seo_title=self.get_seo_title(),
                **kw
            )
        )

    # handle page titles
    # TODO: can I simplify this?
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

    # simpler way to get uris for route handling
    def get_uri(self, name, **kw):
        return webapp2.uri_for(name, **kw)

    def redirect_by_name(self, name, **kw):
        self.redirect(self.get_uri(name, **kw))

    # Check if a user is logged in and return that User object
    def get_loggedin_user(self):
        u_id = auth.get_user_cookie_id(self)
        if u_id:
            return User.get_by_id(int(u_id))

    # TODO: should this be moved, and can returns be removed
    # returns whether current user can edit post
    def user_can_edit(self):
        return (self.u and self.p) and self.u.can_edit_post(self.p)

    # returns whether user can like post
    def user_can_like(self):
        return (self.u and self.p) and self.u.can_like_post(self.p)

    # on every page load, save user object to instance variable
    def initialize(self, request, response):
        super(Handler, self).initialize(request, response)
        self.u = self.get_loggedin_user()
        # if there isn't a logged in user, clear user cookies
        if not self.u:
            auth.clear_user_cookie(self)

class FrontPageHandler(Handler):
    POSTS_PER_PAGE = 10

    def get(self):
        cursor = Cursor(urlsafe=self.request.get('cursor'))
        posts, next_cursor, more = Post.get_n(self.POSTS_PER_PAGE, cursor)

        # next cursor to ouput to url
        # next_cursor.urlsafe()

        # TODO: can I fix up uri handling some more?
        self.render('frontpage.html', posts=posts, uri_handler=self.get_uri)

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
            User.signup(self, email, pw, displayname)
            self.redirect_by_name('welcome')

class WelcomeHandler(Handler):
    page_title = 'Welcome'

    def get(self):
        if not self.u:
            self.redirect_by_name('login')
        else:
            displayname = self.u.get_displayname()
            self.render('welcome.html', displayname=displayname)

class LoginHandler(Handler):
    page_title = 'Login'

    def get(self):
        self.render('login.html')

    def post(self):
        email = self.request.get('email')
        pw = self.request.get('password')

        u = User.get_by_email(email)

        errors = validate.login_errors(email, pw, u)

        if errors:
            self.render('login.html', email=email, errors=errors)
        else:
            auth.set_user_cookie(self, u.key)
            self.redirect_by_name('welcome')

class LogoutHandler(Handler):
    def get(self):
        if self.u:
            auth.clear_user_cookie(self)
        self.redirect_by_name('login')

class EditPostHandler(Handler):
    # TODO: need to finetune this
    page_title = 'Edit Post'

    def get(self):
        post_id = self.request.get('post_id')
        self.p = Post.get_by_id(int(post_id))
        if self.user_can_edit():
            post_url = self.get_uri('singlepost', post_id=post_id)
            self.render(
                'editpost.html',
                title=self.p.title,
                body=self.p.body,
                post_id=post_id,
                post_url=post_url)
        else:
            # TODO: need to handle error messages
            error_msg = 'You cannot edit this post.'
            self.render('error.html', error_msg=error_msg)

    def post(self):
        post_id = self.request.get('post_id')
        self.p = Post.get_by_id(int(post_id))
        if self.user_can_edit():
            title = self.request.get('title')
            body = self.request.get('body')

            post_url = self.get_uri('singlepost', post_id=post_id)

            #check for errors
            errors = validate.editpost_errors(title, body)

            if errors:
                self.render(
                    'editpost.html',
                    title=title,
                    body=body,
                    post_id=post_id,
                    post_url=post_url,
                    errors=errors)
            else:
                msg = 'Post successfully updated.'
                self.p.update(title, body)
                self.render(
                    'editpost.html',
                    title=self.p.title,
                    body=self.p.body,
                    post_id=post_id,
                    post_url=post_url,
                    msg=msg)
        else:
            error_msg = 'You cannot edit this post.'
            self.render('error.html', error_msg=error_msg)


class NewPostHandler(Handler):
    page_title = 'New Post'

    def get(self):
        if not self.u:
            self.redirect_by_name('login')
        else:
            self.render('newpost.html')

    def post(self):
        if not self.u:
            self.redirect_by_name('login')
        else:
            title = self.request.get('title')
            body = self.request.get('body')

            errors = validate.newpost_errors(title, body)

            if errors:
                self.render(
                    'newpost.html',
                    title=title,
                    body=body,
                    errors=errors)
            else:
                p_key = Post.create(title, body, self.u)
                p_uri = self.get_uri('singlepost', post_id=p_key.id())
                self.redirect(p_uri)

class SinglePostHandler(Handler):
    # TODO: add blog
    # add comments
    # add ability to edit
    def initialize(self, request, response):
        super(SinglePostHandler, self).initialize(request, response)
        p_id = int(self.request.route_kwargs['post_id'])
        self.p = Post.get_by_id(p_id)
        self.page_title = self.p.title

    # TODO: add comment display, edit, delete logic here
    def render_post(self, **kw):
        comments = Comment.get_post_comments(self.p)
        self.render(
            'singlepost.html',
            p=self.p,
            comments=comments,
            **kw
        )

    # render post for a logged in user
    def render_post_user(self, **kw):
        edit_url = self.get_uri('editpost')
        can_comment = True
        can_edit = self.user_can_edit()
        can_like = self.user_can_like()
        liked_post = self.u.liked_post(self.p)
        self.render_post(
            edit_url=edit_url,
            can_comment=can_comment,
            can_edit=can_edit,
            can_like = can_like,
            liked_post = liked_post,
            **kw)

    def get(self, post_id):
        # check if post author is logged in author
        # TODO: handle errors if post does not exist, or author not logged in
        if self.u:
            self.render_post_user()
        else:
            self.render_post()

    # TODO: does this keep posting if user not logged in?
    # TODO: we need methods to check these on users
    def post(self, post_id):
        action = self.request.get('action')
        if self.u and action == 'comment':
            # user action to comment
            comment_body = self.request.get('comment_body')
            if comment_body:
                Comment.create(comment_body, self.u, self.p)
                self.redirect_by_name('singlepost', post_id=post_id)
            else:
                # blank comment submitted
                errors = {}
                errors['comment_body'] = 'Comment cannot be blank.'
                self.render_post_user(comment_body=comment_body, errors=errors)
        elif self.u and not self.user_can_edit() and action:
            # user action to like or unlike
            # TODO: perhaps action can be like, and another says like/unlike
            if action == 'like':
                self.u.like(self.p)
            elif action == 'unlike':
                self.p.remove_like(self.u.key)
            self.render_post_user()
        else:
            # if no user or no action to post, redirect user
            self.redirect_by_name('singlepost', post_id=post_id)

# TODO: Handling with or without backslash
app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=FrontPageHandler, name='frontpage'),
    webapp2.Route('/signup', handler=SignUpHandler, name='signup'),
    webapp2.Route('/welcome', handler=WelcomeHandler, name='welcome'),
    webapp2.Route('/login', handler=LoginHandler, name='login'),
    webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
    webapp2.Route('/newpost', handler=NewPostHandler, name='newpost'),
    webapp2.Route('/post/<post_id:[0-9]+>', handler=SinglePostHandler, name='singlepost'),
    webapp2.Route('/editpost', handler=EditPostHandler, name='editpost')
], debug=True)
