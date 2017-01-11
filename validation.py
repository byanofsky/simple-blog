from functools import wraps

from google.appengine.ext import ndb

import auth


def get_user(f):
    @wraps(f)
    def wrapper(self, *a, **kw):
        user_id = auth.get_user_cookie_id(self)
        if user_id:
            user = ndb.Key('User', int(user_id)).get()
        else:
            user = None
        if not user:
            # if there isn't a logged in user, clear user cookies
            auth.clear_user_cookie(self)
        return f(self, user, *a, **kw)
    return wrapper


def require_user(f):
    @wraps(f)
    # TODO: is this setup correct
    @get_user
    def wrapper(self, user, *a, **kw):
        if user:
            return f(self, user, *a, **kw)
        else:
            self.abort(404)
            return
    return wrapper


# TODO: is this something that can be handled with errors and exceptions?
def require_user_or_redirect(redirect_name):
    def decorated_function(f):
        @wraps(f)
        @get_user
        def wrapper(self, user, *a, **kw):
            if user:
                return f(self, user, *a, **kw)
            else:
                self.redirect_to(redirect_name)
                return
        return wrapper
    return decorated_function


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
# comment_exists
# user_logged_in
# user_owns_post
# user_owns_comment
