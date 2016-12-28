import re

USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
PASSWORD_RE = re.compile(r'^.{3,20}$')
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_username(un):
    return USER_RE.match(un)

def valid_password(pw):
    return PASSWORD_RE.match(pw)

def password_match(pw, verify):
    return pw == verify

def valid_email(email):
    return EMAIL_RE.match(email)

def signup_errors(un, pw, verify, email):
    errors = {}

    if not valid_username(un):
        errors['username'] = ('Please enter a valid username. 3-20 characters,'
                              ' using only letters, numbers, "_", or "-".')
    if not valid_password(pw):
        errors['password'] = 'Please enter a valid password. 3-20 characters.'
    if not password_match(pw, verify):
        errors['verify'] = ('Your passwords do not match. Please ' +
                                    're-enter your passwords.')
    if email and not valid_email(email):
        errors['email'] = 'Please enter a valid email address.'

    return errors
