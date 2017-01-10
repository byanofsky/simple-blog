from handlers.basehandler import BaseHandler


class WelcomeHandler(BaseHandler):
    page_title = 'Welcome'

    def get(self):
        if not self.u:
            # if no user signed in, redirect to login
            self.redirect_to('login')
        else:
            self.render('welcome.html', displayname=self.u.get_displayname(),
                        uri_for=self.get_uri)
