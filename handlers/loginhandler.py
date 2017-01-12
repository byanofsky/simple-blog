from handlers.basehandler import BaseHandler
from models.user import User
import modules.form_validation as validate
import modules.auth
# TODO: can we get rid of so many imports? User, auth, validate


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        # Get Login POST data
        email = self.request.get('email')
        pw = self.request.get('password')
        user = User.get_by_email(email)

        # TODO: Can this be moved into one function?
        # TODO: Could return errors, user, in one function
        # u, error = check_login()

        # Check for login form errors
        errors = validate.login_errors(user, email, pw)

        if errors:
            # If form errors, display form with errors
            self.render('login.html', email=email, errors=errors)
        else:
            # If form validates, set user cookie and direct to welcome page
            auth.set_user_cookie(self, user.key)
            self.redirect_to('welcome')
