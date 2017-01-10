from handlers.basehandler import BaseHandler


class LogoutHandler(BaseHandler):
    def get(self):
        # TODO: move to its own function
        # If there is a user logged in, clear cookies.
        if self.u:
            auth.clear_user_cookie(self)
        self.redirect_to('login')
