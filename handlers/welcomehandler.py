from handlers.basehandler import BaseHandler
from modules.validation import require_user_or_redirect


class WelcomeHandler(BaseHandler):
    @require_user_or_redirect('login')
    def get(self, user):
        self.render('welcome.html', user=user)
