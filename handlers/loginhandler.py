from handlers.basehandler import BaseHandler
import modules.user_auth as user_auth
# TODO: can we get rid of so many imports? User, auth, validate


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        # Get Login POST data
        email = self.request.get('email')
        pw = self.request.get('password')

        # Check for login form errors
        errors, user = user_auth.validate_login(email, pw)
        if errors:
            self.render('login.html', email=email, errors=errors)
        else:
            # If form validates, set user cookie and direct to welcome page
            self.set_secure_cookie('user_id', user.key.id())
            self.redirect_to('welcome')
