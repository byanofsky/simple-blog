import os
import yaml

import jinja2
import webapp2

import validate
import auth
from datacls import Post, Comment, User
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb

# load config settings
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# Jinja templating setup
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True,
)


# TODO: can we move these classes to their own files and not reimport?
class Handler(webapp2.RequestHandler):
    site_title = cfg['site_title']

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
        self.write(
            self.render_str(
                template,
                page_title=self.get_page_title(),
                seo_title=self.get_seo_title(),
                **kw
            )
        )

    # Handles HTML title tag
    def get_seo_title(self):
        if hasattr(self, 'page_title') and self.page_title:
            return self.page_title + " - " + self.site_title
        else:
            return self.site_title

    # Handles visible title on pages
    def get_page_title(self):
        if hasattr(self, 'page_title') and self.page_title:
            return self.page_title
        else:
            return self.site_title

    # simpler way to get uris for route handling
    # TODO: can this be removed?
    # TODO: Replace with uri_for
    def get_uri(self, name, **kw):
        return webapp2.uri_for(name, **kw)

    # Helper for returning a singlepost uri
    def get_post_uri(self, post):
        return self.get_uri('singlepost', post_id=post.key.id())

    # Redirect to the error handler
    def error_redirect(self, code, **kw):
        self.redirect_to('error', code=code, **kw)

    # Redirect to the success handler
    def success_redirect(self, code, **kw):
        self.redirect_to('success', code=code, **kw)

    # Check if a user is logged in.
    # If there is a user, return that User object.
    def get_loggedin_user(self):
        u_id = auth.get_user_cookie_id(self)
        if u_id:
            return User.get_by_id(int(u_id))

    # On page load, save user object to instance variable
    def initialize(self, request, response):
        super(Handler, self).initialize(request, response)
        self.u = self.get_loggedin_user()
        # if there isn't a logged in user, clear user cookies
        if not self.u:
            auth.clear_user_cookie(self)


class FrontPageHandler(Handler):
    # Constant for how many posts to display per page
    POSTS_PER_PAGE = 10

    def get(self):
        cursor = Cursor(urlsafe=self.request.get('cursor'))
        posts, next_cursor, more = Post.get_n(self.POSTS_PER_PAGE, cursor)

        # TODO: code for building multi-page frontpage
        # next cursor to ouput to url
        # next_cursor.urlsafe()

        # TODO: can I fix up uri handling some more?
        self.render('frontpage.html', posts=posts, uri_for=self.get_post_uri)


class SignUpHandler(Handler):
    page_title = 'Signup'

    def get(self):
        self.render('signup.html', login=self.uri_for('login'))

    def post(self):
        # Save POST data
        email = self.request.get('email')
        pw = self.request.get('password')
        verify = self.request.get('verify')
        displayname = self.request.get('displayname')

        # Validate signup form data
        errors = validate.signup_errors(
            email, pw, verify,
            user_exists=User.get_by_email(email)
        )

        if errors:
            self.render('signup.html', login=self.uri_for('login'),
                        email=email, displayname=displayname, errors=errors)
        else:
            # If form data is ok, add user to database and direct to
            # welcome page.
            User.signup(self, email, pw, displayname)
            self.redirect_to('welcome')


class WelcomeHandler(Handler):
    page_title = 'Welcome'

    def get(self):
        if not self.u:
            # if no user signed in, redirect to login
            self.redirect_to('login')
        else:
            self.render('welcome.html', displayname=self.u.get_displayname(),
                        uri_for=self.get_uri)


class LoginHandler(Handler):
    page_title = 'Login'

    def get(self):
        self.render('login.html', signup=self.uri_for('signup'))

    def post(self):
        # Get Login POST data
        email = self.request.get('email')
        pw = self.request.get('password')
        u = User.get_by_email(email)

        # TODO: Can this be moved into one function?
        # TODO: Could return errors, user, in one function
        # u, error = check_login()

        # Check for login form errors
        errors = validate.login_errors(email, u, pw)

        if errors:
            # If form errors, display form with errors
            self.render('login.html', email=email, errors=errors,
                        signup=self.uri_for('signup'))
        else:
            # If form validates, set user cookie and direct to welcome page
            auth.set_user_cookie(self, u.key)
            self.redirect_to('welcome')


class LogoutHandler(Handler):
    def get(self):
        # TODO: move to its own function
        # If there is a user logged in, clear cookies.
        if self.u:
            auth.clear_user_cookie(self)
        self.redirect_to('login')


class SinglePostHandler(Handler):
    def initialize(self, request, response):
        super(SinglePostHandler, self).initialize(request, response)
        # Get post_id from route
        self.p_id = int(self.request.route_kwargs['post_id'])
        # Save post object
        self.p = Post.get_by_id(self.p_id)
        # Set post title as page title
        self.page_title = self.p.title

    # TODO: can render post be combined into one function
    # TODO: add comment display, edit, delete logic here
    # Helper for singlepost jinja template
    def render_post(self, **kw):
        self.render('singlepost.html', p=self.p,
                    comments=Comment.get_comments(self.p), **kw)

    # Extends render_post for a logged in user
    def render_post_user(self, **kw):
        self.render_post(
            edit_post_uri=self.get_uri('editpost', post_id=self.p_id),
            uri_for=self.get_uri,
            can_comment=True,
            user=self.u,
            can_edit=self.u.can_edit(self.p),
            can_like=self.u.can_like_post(self.p),
            liked_post=self.u.liked_post(self.p),
            **kw)

    def get(self, post_id):
        # TODO: handle errors if post does not exist
        if self.u:
            self.render_post_user()
        else:
            self.render_post()

    def post(self, post_id):
        # Get query string data for "action"
        action = self.request.get('action')
        # The actions that are currently possible on singlepost
        action_list = ['comment', 'like', 'unlike']
        if self.u and (action in action_list):
            if action == 'comment':
                # Process comment form
                comment = self.request.get('comment')
                errors = validate.comment_errors(comment)
                if errors:
                    self.render_post_user(comment=comment, errors=errors)
                else:
                    self.u.leave_comment(comment, self.p)
                    self.redirect_to('singlepost', post_id=post_id)
            else:
                # If action isn't comment, it must be like or unlike.
                # Uses "else" instead of "elif" so redirect can be used.
                if action == 'like':
                    self.u.like(self.p)
                elif action == 'unlike':
                    self.u.unlike(self.p)
                self.redirect_to('singlepost', post_id=post_id)
        else:
            # If no user or no action, redirect user to post
            self.redirect_to('singlepost', post_id=post_id)


class NewPostHandler(Handler):
    page_title = 'New Post'

    def get(self):
        if self.u:
            self.render('newpost.html')
        else:
            self.error_redirect('createpost')

    def post(self):
        if self.u:
            title = self.request.get('title')
            body = self.request.get('body')
            # Validate newpost form
            errors = validate.newpost_errors(title, body)

            if errors:
                self.render('newpost.html', title=title, body=body,
                            errors=errors)
            else:
                # Create post in database, and redirect to singlepost
                p_key = Post.create(title, body, self.u)
                self.redirect_to('singlepost', post_id=p_key.id())
        else:
            # If no user logged in, redirect to error page
            self.error_redirect('createpost')


# TODO: combine error and success
# This handles errors, such as when visitor tries to edit
# someone else's posts.
class ErrorHandler(Handler):
    page_title = 'Error'

    def get(self):
        # Get error code passed
        code = self.request.get('code')
        if code == 'editpost':
            error_msg = 'You cannot edit this post.'
            back_url = self.uri_for('frontpage')
            back_text = 'Go to homepage.'
        elif code == 'editcomment' and self.request.get('post'):
            # Get post key passed to allow redirect back to post
            p_key = ndb.Key(urlsafe=self.request.get('post'))
            error_msg = 'You cannot edit this comment.'
            back_url = self.uri_for('singlepost', post_id=p_key.id())
            back_text = 'Go back to post.'
        elif code == 'createpost':
            error_msg = 'You must be logged in to create a post.'
            back_url = self.uri_for('login')
            back_text = 'Login.'
        else:
            error_msg = 'There was an error.'
            back_url = self.uri_for('frontpage')
            back_text = 'Go to homepage.'
        self.render('notice.html', msg=error_msg, url=back_url, text=back_text)


# This handles success messages, such as after deleting a comment
class SuccessHandler(Handler):
    page_title = 'Success'

    def get(self):
        # Get success code
        code = self.request.get('code')
        if code == 'postdelete':
            success_msg = 'Post deleted.'
            next_url = self.uri_for('frontpage')
            next_text = 'Go to homepage'
        elif code == 'commentdelete' and self.request.get('post'):
            # Get post key to allow return to post
            p_key = ndb.Key(urlsafe=self.request.get('post'))
            success_msg = 'Comment deleted.'
            next_url = self.uri_for('singlepost', post_id=p_key.id())
            next_text = 'Back to post'
        else:
            success_msg = 'Action completed successfully.'
            next_url = self.uri_for('frontpage')
            next_text = 'Go to homepage'
        self.render('notice.html', msg=success_msg, url=next_url,
                    text=next_text)


class EditPostHandler(Handler):
    # TODO: need to finetune this
    page_title = 'Edit Post'

    def initialize(self, request, response):
        super(EditPostHandler, self).initialize(request, response)
        # initialize post object
        self.p = Post.get_by_id(int(self.request.get('post_id')))

    # TODO: need a render post function
    def render_edit_page(self, **kw):
        # TODO: this may be bad since it is getting post id again for post_uri
        self.render('editpost.html', p=self.p,
                    post_uri=self.get_post_uri(self.p), **kw)

    def get(self):
        # Check if logged in user can edit this post
        if self.u and self.u.can_edit(self.p):
            self.render_edit_page()
        else:
            self.error_redirect('editpost')

    def post(self):
        # Check if logged in user can edit this post
        if self.u and self.u.can_edit(self.p):
            # TODO: are there are any issues here with security
            # (if someone deletes anothers post)
            action = self.request.get('action')
            if action == 'delete':
                self.p.delete()
                self.success_redirect('postdelete')
            # TODO: need an edit action here
            # If action isn't delete, then it is to edit post
            else:
                # User used editpost form
                title = self.request.get('title')
                body = self.request.get('body')
                # Check editpost form for errors
                errors = validate.editpost_errors(title, body)

                if errors:
                    msg = ('Your post was not edited.' +
                           'Please fix errors and resubmit.')
                    self.render_edit_page(title=title, body=body, msg=msg,
                                          errors=errors)
                else:
                    # No errors, update post
                    msg = 'Post successfully updated.'
                    self.p.update(title, body)
                    # TODO: should we redirect so user can't go back and post?
                    self.render_edit_page(msg=msg)
        else:
            # If no user logged in, redirect to error page
            self.error_redirect('editpost')


class EditCommentHandler(Handler):
    # TODO: need to finetune this like edit post
    # TODO: can combine with editpost?
    page_title = 'Edit Comment'

    def initialize(self, request, response):
        super(EditCommentHandler, self).initialize(request, response)
        # Initialize comment object
        # TODO: fix this up
        c_key = ndb.Key(urlsafe=self.request.get('comment_key'))
        self.c = c_key.get()
        # Initialize post object from comment parent
        self.p = c_key.parent().get()

    def render_edit_page(self, **kw):
        # TODO: this may be bad since it is getting post id again
        # TODO: need to get parent post url
        self.render('editcomment.html', c=self.c,
                    post_uri=self.get_post_uri(self.p), **kw)

    def get(self):
        # Check if user can edit comment
        if self.u and self.u.can_edit(self.c):
            self.render_edit_page()
        else:
            # If user can't edit comment, redirect to error page
            self.error_redirect('editcomment', post=self.p.key.urlsafe())

    def post(self):
        if self.u and self.u.can_edit(self.c):
            # TODO: are there are any issues here with security.
            # Such as if someone deletes anothers post.

            # Check user's action
            action = self.request.get('action')
            if action == 'delete':
                self.c.delete()
                self.success_redirect('commentdelete',
                                      post=self.p.key.urlsafe())
            elif action == 'update':
                body = self.request.get('body')
                # Check editcomment form for errors
                errors = validate.editcomment_errors(body)
                if errors:
                    msg = ('Your comment was not edited.' +
                           'Please fix errors and resubmit.')
                    self.render_edit_page(body=body, msg=msg, errors=errors)
                else:
                    # TODO: what if not updated?
                    self.c.update(body)
                    msg = 'Comment successfully updated.'
                    self.render_edit_page(msg=msg)
            else:
                # If action is not delete or update
                msg = 'No changes made.'
                self.render_edit_page(msg=msg)
        else:
            # If no user logged in or user can't edit comment,
            # redirect to error page
            self.error_redirect('editcomment', post=self.p.key.urlsafe())


# TODO: Handling with or without backslash
app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=FrontPageHandler, name='frontpage'),
    webapp2.Route('/signup', handler=SignUpHandler, name='signup'),
    webapp2.Route('/welcome', handler=WelcomeHandler, name='welcome'),
    webapp2.Route('/login', handler=LoginHandler, name='login'),
    webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
    webapp2.Route('/newpost', handler=NewPostHandler, name='newpost'),
    webapp2.Route('/post/<post_id:[0-9]+>', handler=SinglePostHandler,
                  name='singlepost'),
    webapp2.Route('/editpost', handler=EditPostHandler, name='editpost'),
    webapp2.Route('/editcomment', handler=EditCommentHandler,
                  name='editcomment'),
    webapp2.Route('/error', handler=ErrorHandler, name='error'),
    webapp2.Route('/success', handler=SuccessHandler, name='success')
], debug=True)
