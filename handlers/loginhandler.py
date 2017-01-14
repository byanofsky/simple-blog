from handlers.basehandler import BaseHandler
import modules.user_auth as user_auth


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        # Get Login POST data
        email = self.request.get('email')
        pw = self.request.get('password')

        # Check for login errors
        # TODO: can this be simplified? Might be with exceptions
        errors, user = user_auth.validate_login(email, pw)
        valid_login = user and not errors

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
