from handlers.basehandler import BaseHandler
import modules.user_auth as user_auth


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
        errors, user_key = user_auth.validate_signup(
            email=email,
            pw=pw,
            verify_pw=verify_pw,
            displayname=displayname
        )

        if errors:
            self.render(
                'signup.html',
                email=email,
                displayname=displayname,
                errors=errors
            )
        else:
            # No errors and user created
            user_id = user_key.id()
            # Set secure cookie value and redirect to welcome page
            self.set_secure_cookie('user_id', user_id)
            self.redirect_to('welcome')
