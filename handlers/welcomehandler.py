from handlers.basehandler import BaseHandler
from modules.validation import require_user


class WelcomeHandler(BaseHandler):
    @require_user('login')
    def get(self, user):
        self.render('welcome.html', user=user)
