from handlers.basehandler import BaseHandler
import modules.secure as secure
import modules.form_validation as form_validation
from models.user import User
# TODO: can we get rid of so many imports? User, auth, validate


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        # Default state
        user = None
        valid_login = False

        # Get Login POST data
        email = self.request.get('email')
        pw = self.request.get('password')

        # Check for login form errors
        # TODO: can this be simplified? Might be with exceptions
        errors = form_validation.check_login(email, pw)
        if not errors:
            # Let's get user associated with email
            user = User.get_by_email(email)
            if not user:
                # User does not exist. Set error.
                errors['user'] = True
            else:
                # User does exist, so let's check if
                # pw entered matches hashed_pw.
                valid_login = secure.verify_pw(pw, user.hashed_pw)
                if not valid_login:
                    # Password is incorrect
                    errors['login'] = True

        if valid_login:
            # If form validates, set user cookie and direct to welcome page
            self.set_secure_cookie('user_id', user.key.id())
            self.redirect_to('welcome')
        else:
            self.render(
                'login.html',
                email=email,
                errors=errors
            )
