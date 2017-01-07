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
    # trim_blocks = True,
    # lstrip_blocks = True
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

    def get_post_uri(self, post):
        return self.get_uri('singlepost', post_id=post.key.id())

    def redirect_by_name(self, name, **kw):
        self.redirect(self.get_uri(name, **kw))

    def error_redirect(self, code, **kw):
        self.redirect_to('error', code=code, **kw)

    def success_redirect(self, code, **kw):
        self.redirect_to('success', code=code, **kw)

    # Check if a user is logged in and return that User object
    def get_loggedin_user(self):
        u_id = auth.get_user_cookie_id(self)
        if u_id:
            return User.get_by_id(int(u_id))

    # returns whether user can like post
    # TODO: remove
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

    def render_posts(self, posts):
        post_loop = ''
        for post in posts:
            post_loop += self.render_str('post.html', post=post)
        return post_loop

    def get(self):
        cursor = Cursor(urlsafe=self.request.get('cursor'))
        posts, next_cursor, more = Post.get_n(self.POSTS_PER_PAGE, cursor)

        # next cursor to ouput to url
        # next_cursor.urlsafe()

        # TODO: can I fix up uri handling some more?
        self.render(
            'frontpage.html',
            posts=posts,
            uri_for=self.get_post_uri
        )

class SignUpHandler(Handler):
    page_title = 'Signup'

    def get(self):
        self.render('signup.html')

    def post(self):
        email = self.request.get('email')
        pw = self.request.get('password')
        verify = self.request.get('verify')
        displayname = self.request.get('displayname')

        # TODO: move into a function

        # Validate signup
        errors = validate.signup_errors(
            email,
            pw,
            verify,
            user_exists = User.get_by_email(email)
        )

        if errors:
            self.render(
                'signup.html',
                email=email,
                displayname=displayname,
                errors=errors
            )
        else:
            User.signup(self, email, pw, displayname)
            self.redirect_by_name('welcome')

class WelcomeHandler(Handler):
    page_title = 'Welcome'

    def get(self):
        # if no user signed in, redirect to login
        if not self.u:
            self.redirect_by_name('login')
        # when user signed in, display welcome page
        else:
            self.render(
                'welcome.html',
                displayname=self.u.get_displayname(),
                uri_for=self.get_uri
            )

class LoginHandler(Handler):
    page_title = 'Login'

    def get(self):
        self.render('login.html')

    def post(self):
        email = self.request.get('email')
        pw = self.request.get('password')
        u = User.get_by_email(email)

        # TODO: can this be moved into one function?
        # TODO: could return errors, user, in one function
        # u, error = check_login()
        errors = validate.login_errors(email, u, pw)

        if errors:
            self.render('login.html', email=email, errors=errors)
        else:
            auth.set_user_cookie(self, u.key)
            self.redirect_by_name('welcome')

class LogoutHandler(Handler):
    def get(self):
        # TODO: move to its own function
        if self.u:
            auth.clear_user_cookie(self)
        self.redirect_by_name('login')

class SinglePostHandler(Handler):
    def initialize(self, request, response):
        super(SinglePostHandler, self).initialize(request, response)
        # initialize post object
        self.p_id = int(self.request.route_kwargs['post_id'])
        self.p = Post.get_by_id(self.p_id)
        # set post title
        self.page_title = self.p.title

    # TODO: can render post be combined into one function
    # TODO: add comment display, edit, delete logic here
    def render_post(self, **kw):
        self.render(
            'singlepost.html',
            p=self.p,
            comments=Comment.get_comments(self.p),
            **kw
        )

    # render post for a logged in user
    def render_post_user(self, **kw):
        self.render_post(
            edit_post_uri=self.get_uri('editpost', post_id=self.p_id),
            uri_for=self.get_uri,
            can_comment=True,
            user=self.u,
            can_edit=self.u.can_edit(self.p),
            can_like=self.u.can_like_post(self.p),
            liked_post=self.u.liked_post(self.p),
            **kw
        )

    def get(self, post_id):
        # TODO: handle errors if post does not exist
        if self.u:
            self.render_post_user()
        else:
            self.render_post()

    def post(self, post_id):
        action = self.request.get('action')
        action_list = ['comment', 'like', 'unlike']
        if self.u and (action in action_list):
            # TODO: display error if try to do action not able to
            if action == 'comment':
                # TODO: can this be moved to its own function
                comment = self.request.get('comment')
                errors = validate.comment_errors(comment)

                if errors:
                    self.render_post_user(comment=comment, errors=errors)
                else:
                    self.u.leave_comment(comment, self.p)
                    self.redirect_by_name('singlepost', post_id=post_id)

            else:
                if action == 'like':
                    # user action to like or unlike
                    self.u.like(self.p)

                if action == 'unlike':
                    self.u.unlike(self.p)

                self.redirect_by_name('singlepost', post_id=post_id)
        else:
            # if no user or no action to post, redirect user
            self.redirect_by_name('singlepost', post_id=post_id)


class NewPostHandler(Handler):
    page_title = 'New Post'

    def render_newpost(self, **kw):
        self.render('newpost.html', **kw)

    def get(self):
        if self.u:
            self.render_newpost()
        else:
            self.error_redirect('createpost')

    def post(self):
        if self.u:
            title = self.request.get('title')
            body = self.request.get('body')

            errors = validate.newpost_errors(title, body)

            if errors:
                self.render_newpost(
                    title=title,
                    body=body,
                    errors=errors
                )
            else:
                p_key = Post.create(title, body, self.u)
                self.redirect_by_name('singlepost', post_id=p_key.id())
        else:
            # TODO: this may need to be a redirect so it doesn't keep posting
            self.error_redirect('createpost')

# TODO: move this
# class StatusHandler(Handler):
#     def get(self):

class ErrorHandler(Handler):
    page_title = 'Error'

    def get(self):
        code = self.request.get('code')
        p_key = ndb.Key(urlsafe=self.request.get('post'))

        if code == 'editpost':
            error_msg = 'You cannot edit this post.'
            back_text = 'Go to homepage.'
            back_url = self.uri_for('frontpage')

        elif code == 'editcomment':
            error_msg = 'You cannot edit this comment.'
            back_text = 'Go back to post.'
            # TODO: how can user go back to post
            back_url = self.uri_for('singlepost', post_id=p_key.id())

        elif code == 'createpost':
            error_msg = 'You must be logged in to create a post.'
            back_text = 'Login.'
            back_url = self.uri_for('login')

        else:
            error_msg = 'There was an error.'
            back_text = 'Go to homepage.'
            back_url = self.uri_for('frontpage')

        self.render(
            'notice.html',
            msg=error_msg,
            url=back_url,
            text=back_text
        )

class SuccessHandler(Handler):
    page_title = 'Success'

    def get(self):
        code = self.request.get('code')
        p_key = ndb.Key(urlsafe=self.request.get('post'))

        if code == 'postdelete':
            success_msg = 'Post deleted.'
            next_url = self.uri_for('frontpage')
            next_text = 'Go to homepage'

        elif code == 'commentdelete':
            success_msg = 'Comment deleted.'
            # TODO: how can user go back to post
            next_url = self.uri_for('singlepost', post_id=p_key.id())
            next_text = 'Back to post'

        self.render(
            'notice.html',
            msg=success_msg,
            url=next_url,
            text=next_text
        )

class EditPostHandler(Handler):
    # TODO: need to finetune this
    page_title = 'Edit Post'

    def initialize(self, request, response):
        super(EditPostHandler, self).initialize(request, response)
        # initialize post object
        self.p = Post.get_by_id(int(self.request.get('post_id')))

    # TODO: need a render post function
    def render_edit_page(self, **kw):
        self.render(
            'editpost.html',
            p=self.p,
            # TODO: this may be bad since it is getting post id again
            post_uri=self.get_post_uri(self.p),
            **kw
        )

    def get(self):
        if self.u and self.u.can_edit(self.p):
            self.render_edit_page()
        else:
            # error_msg = 'You cannot edit this post.'
            self.error_redirect('editpost')

    def post(self):
        if self.u and self.u.can_edit(self.p):
            # TODO: are there are any issues here with security (if someone deletes anothers post)
            action = self.request.get('action')
            if action == 'delete':
                self.p.delete()
                self.success_redirect('postdelete')
            else:
                title = self.request.get('title')
                body = self.request.get('body')

                #check for errors
                errors = validate.editpost_errors(title, body)

                if errors:
                    msg = 'Your post was not edited. Please fix errors and resubmit.'
                    self.render_edit_page(
                        title=title,
                        body=body,
                        msg=msg,
                        errors=errors
                    )
                else:
                    msg = 'Post successfully updated.'
                    # TODO: what if not updated?
                    self.p.update(title, body)
                    self.render_edit_page(msg=msg)
        else:
            self.error_redirect('editpost')

class EditCommentHandler(Handler):
    # TODO: need to finetune this like edit post
    # TODO: can combine with editpost?
    page_title = 'Edit Comment'

    def initialize(self, request, response):
        super(EditCommentHandler, self).initialize(request, response)
        # initialize comment object
        # TODO: fix this up
        c_key = ndb.Key(urlsafe=self.request.get('comment_key'))
        self.c = c_key.get()
        # initialize parent post object
        self.p = c_key.parent().get()

    # TODO: need a render post function
    def render_edit_page(self, **kw):
        self.render(
            'editcomment.html',
            c=self.c,
            # TODO: this may be bad since it is getting post id again
            # TODO: need to get parent post url
            post_uri=self.get_post_uri(self.p),
            **kw
        )

    def get(self):
        if self.u and self.u.can_edit(self.c):
            self.render_edit_page()
        else:
            self.error_redirect('editcomment', post=self.p.key.urlsafe())

    def post(self):
        if self.u and self.u.can_edit(self.c):
            # TODO: are there are any issues here with security (if someone deletes anothers post)
            action = self.request.get('action')
            if action == 'delete':
                self.c.delete()
                self.success_redirect('commentdelete', post=self.p.key.urlsafe())
            elif action == 'update':
                body = self.request.get('body')

                #check for errors
                errors = validate.editcomment_errors(body)

                if errors:
                    msg = 'Your comment was not edited. Please fix errors and resubmit.'
                    self.render_edit_page(
                        body=body,
                        msg=msg,
                        errors=errors
                    )
                else:
                    msg = 'Comment successfully updated.'
                    # TODO: what if not updated?
                    self.c.update(body)
                    self.render_edit_page(msg=msg)
            else:
                msg = 'No changes made.'
                self.c.update(body)
                self.render_edit_page(msg=msg)

        else:
            self.error_redirect('editcomment', post=self.p.key.urlsafe())



# TODO: Handling with or without backslash
app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=FrontPageHandler, name='frontpage'),
    webapp2.Route('/signup', handler=SignUpHandler, name='signup'),
    webapp2.Route('/welcome', handler=WelcomeHandler, name='welcome'),
    webapp2.Route('/login', handler=LoginHandler, name='login'),
    webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
    webapp2.Route('/newpost', handler=NewPostHandler, name='newpost'),
    webapp2.Route('/post/<post_id:[0-9]+>', handler=SinglePostHandler, name='singlepost'),
    webapp2.Route('/editpost', handler=EditPostHandler, name='editpost'),
    webapp2.Route('/editcomment', handler=EditCommentHandler, name='editcomment'),
    webapp2.Route('/error', handler=ErrorHandler, name='error'),
    webapp2.Route('/success', handler=SuccessHandler, name='success')
], debug=True)
