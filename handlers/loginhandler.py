from handlers.basehandler import BaseHandler


class LoginHandler(BaseHandler):
    page_title = 'Login'

    def get(self):
        self.render('login.html', signup=self.uri_for('signup'))

    def post(self):
        # Get Login POST data
        email = self.request.get('email')
        pw = self.request.get('password')
        u = User.get_by_email(email)

        # TODO: Can this be moved into one function?
        # TODO: Could return errors, user, in one function
        # u, error = check_login()

        # Check for login form errors
        errors = validate.login_errors(email, u, pw)

        if errors:
            # If form errors, display form with errors
            self.render('login.html', email=email, errors=errors,
                        signup=self.uri_for('signup'))
        else:
            # If form validates, set user cookie and direct to welcome page
            auth.set_user_cookie(self, u.key)
            self.redirect_to('welcome')
