from handlers.basehandler import BaseHandler
from models.user import User
import modules.form_validation as form_validation


class SignUpHandler(BaseHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        # Save POST data
        email = self.request.get('email')
        pw = self.request.get('password')
        verify_pw = self.request.get('verify_pw')
        displayname = self.request.get('displayname')

        # TODO: Might be possible to move below to its own file

        errors = form_validation.check_signup(
            email=email,
            pw=pw,
            verify_pw=verify_pw
        )

        if errors:
            self.render(
                'signup.html',
                email=email,
                displayname=displayname,
                errors=errors
            )
        else:
            # If form data is ok, add user to database
            user_key = User.create(email, pw, displayname)
            user_id = user_key.id()
            # Set secure cookie value and redirect to welcome page
            self.set_secure_cookie('user_id', user_id)
            self.redirect_to('welcome')
