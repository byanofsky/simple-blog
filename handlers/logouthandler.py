from handlers.basehandler import BaseHandler
from modules.validation import get_user
import modules.auth


class LogoutHandler(BaseHandler):
    @get_user
    def get(self, user):
        # Clear user cookies
        # TODO: check out this function
        auth.clear_user_cookie(self)
        self.redirect_to('login')
