from handlers.basehandler import BaseHandler


class SignUpHandler(BaseHandler):
    page_title = 'Signup'

    def get(self):
        self.render('signup.html', login=self.uri_for('login'))

    def post(self):
        # Save POST data
        email = self.request.get('email')
        pw = self.request.get('password')
        verify = self.request.get('verify')
        displayname = self.request.get('displayname')

        # Validate signup form data
        errors = validate.signup_errors(
            email, pw, verify,
            user_exists=User.get_by_email(email)
        )

        if errors:
            self.render('signup.html', login=self.uri_for('login'),
                        email=email, displayname=displayname, errors=errors)
        else:
            # If form data is ok, add user to database and direct to
            # welcome page.
            User.signup(self, email, pw, displayname)
            self.redirect_to('welcome')
