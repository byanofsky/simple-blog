from handlers.basehandler import BaseHandler
from modules.validation import require_user


class LogoutHandler(BaseHandler):
    @require_user('login')
    def get(self, user):
        # Clear user cookies
        self.clear_cookie('user_id')
        self.redirect_to('login')
