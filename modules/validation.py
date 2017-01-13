from functools import wraps

from google.appengine.ext import ndb

import auth


def get_user(f):
    @wraps(f)
    def wrapper(self, *a, **kw):
        user_id = self.get_secure_cookie('user_id')
        if user_id:
            user = ndb.Key('User', int(user_id)).get()
        else:
            user = None
        return f(self, user, *a, **kw)
    return wrapper


def require_user(redirect=None):
    def decorated_function(f):
        @wraps(f)
        @get_user
        def wrapper(self, user, *a, **kw):
            if user:
                return f(self, user, *a, **kw)
            else:
                # If there isn't a logged in user, clear user cookies
                self.clear_cookie('user_id')
                # TODO: is this something that can be handled with errors and exceptions?
                if redirect:
                    self.redirect_to(redirect)
                else:
                    self.abort(404)
        return wrapper
    return decorated_function


# TODO: is this something that can be handled with errors and exceptions?
def require_user_or_redirect(name):
    def decorated_function(f):
        @wraps(f)
        @get_user
        def wrapper(self, user, *a, **kw):
            if user:
                return f(self, user, *a, **kw)
            else:
                self.redirect_to(name)
                return
        return wrapper
    return decorated_function


# Decorator which checks if post exists. And if it does,
# checks if user is the author.
def user_owns_post(f):
    @wraps(f)
    @post_exists
    # TODO: requre user instead
    @get_user
    def wrapper(self, user, post_id, post, *a, **kw):
        if user and user.key == post.author:
            return f(self, user, post_id, post, *a, **kw)
        else:
            # TODO: should this be a redirect or error?
            self.redirect_to('viewpost', post_id=post_id)
            return
    return wrapper


def user_owns_comment(f):
    @wraps(f)
    @comment_exists
    # TODO: requre user instead
    @get_user
    def wrapper(self, user, comment, *a, **kw):
        if user and user.key == comment.author:
            return f(self, user, comment, *a, **kw)
        else:
            # TODO: should this be a redirect or error?
            self.abort(404)
            return
    return wrapper


def user_can_like_post(f):
    @wraps(f)
    @post_exists
    @require_user
    def wrapper(self, user, post_id, post, *a, **kw):
        if user.can_like_post(post):
            return f(self, user, post_id, post, *a, **kw)
        else:
            self.abort(404)
            return
    return wrapper

def user_can_unlike_post(f):
    @wraps(f)
    @post_exists
    @require_user
    def wrapper(self, user, post_id, post, *a, **kw):
        if user.liked_post(post):
            return f(self, user, post_id, post, *a, **kw)
        else:
            self.abort(404)
            return
    return wrapper


def comment_exists(f):
    @wraps(f)
    def wrapper(self, comment_key, *a, **kw):
        # TODO: is there really no better way to handle this?
        try:
            comment = ndb.Key(urlsafe=comment_key).get()
        except ndb.google_imports.ProtocolBuffer.ProtocolBufferDecodeError:
            comment = None
        if comment:
            return f(self, comment, *a, **kw)
        else:
            self.abort(404)
            return
    return wrapper


def post_exists(f):
    @wraps(f)
    def wrapper(self, post_id, *a, **kw):
        post = ndb.Key('Post', int(post_id)).get()
        if post:
            return f(self, post_id, post, *a, **kw)
        else:
            self.abort(404)
            return
    return wrapper
