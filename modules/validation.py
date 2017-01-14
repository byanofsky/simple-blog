from functools import wraps

from google.appengine.ext import ndb


def get_user(f):
    @wraps(f)
    def wrapper(self, *a, **kw):
        # Default user to None
        user = None
        user_id = self.get_secure_cookie('user_id')
        if user_id:
            user = ndb.Key('User', int(user_id)).get()
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
                # TODO: is this something that can be
                # handled with errors and exceptions?
                if redirect:
                    self.redirect_to(redirect)
                else:
                    self.abort(404)
        return wrapper
    return decorated_function


def post_exists(f):
    @wraps(f)
    def wrapper(self, post_id, *a, **kw):
        post = ndb.Key('Post', int(post_id)).get()
        if post:
            return f(self, post, post_id, *a, **kw)
        else:
            self.abort(404)
            return
    return wrapper


# Decorator which checks if post exists. And if it does,
# checks if user is the author.
def user_owns_post(f):
    @wraps(f)
    @post_exists
    @require_user()
    def wrapper(self, user, post, post_id, *a, **kw):
        if user.key == post.author:
            return f(self, user, post, post_id, *a, **kw)
        else:
            # TODO: should this be a redirect or error?
            self.abort(404)
            return
    return wrapper


def comment_exists(f):
    @wraps(f)
    def wrapper(self, url_comment_key, *a, **kw):
        # TODO: is there really no better way to handle this?
        try:
            comment = ndb.Key(urlsafe=url_comment_key).get()
        except ndb.google_imports.ProtocolBuffer.ProtocolBufferDecodeError:
            comment = None
        if comment:
            comment_key = comment.key
            return f(self, comment, comment_key, *a, **kw)
        else:
            self.abort(404)
            return
    return wrapper


def user_owns_comment(f):
    @wraps(f)
    @comment_exists
    # TODO: requre user instead
    @require_user()
    def wrapper(self, user, comment, comment_key, *a, **kw):
        if user.key == comment.author:
            return f(self, user, comment, comment_key, *a, **kw)
        else:
            # TODO: should this be a redirect or error?
            self.abort(404)
            return
    return wrapper


def user_can_like_post(f):
    @wraps(f)
    @post_exists
    @require_user()
    def wrapper(self, user, post, post_id, *a, **kw):
        if user.can_like_post(post):
            return f(self, user, post, post_id, *a, **kw)
        else:
            self.abort(404)
            return
    return wrapper

def user_can_unlike_post(f):
    @wraps(f)
    @post_exists
    @require_user()
    def wrapper(self, user, post, post_id, *a, **kw):
        if user.liked_post(post):
            return f(self, user, post, post_id, *a, **kw)
        else:
            self.abort(404)
            return
    return wrapper
