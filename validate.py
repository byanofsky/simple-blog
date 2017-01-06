import re
from auth import valid_login

PASSWORD_RE = re.compile(r'^.{3,20}$')
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_email(email):
    return EMAIL_RE.match(email)

def valid_password(pw):
    return PASSWORD_RE.match(pw)

def password_match(pw, verify):
    return pw == verify

def signup_errors(email, pw, verify, user_exists):
    errors = {}

    if user_exists:
        errors['user_exists'] = ('There is already a user registered ' +
                                 'with this email.')
    if not valid_email(email):
        errors['email'] = 'Please enter a valid email address.'
    if not valid_password(pw):
        errors['password'] = 'Please enter a valid password. 3-20 characters.'
    if not password_match(pw, verify):
        errors['verify'] = ('Your passwords do not match. Please re-enter ' +
                            'your passwords.')

    return errors

def login_errors(email, u, pw):
    if not valid_email(email):
        return 'Please enter a valid email address.'
    elif not u:
        return 'There is no user with this email address.'
    elif not valid_login(u, pw):
        return 'The password is incorrect. Please try again.'

def newpost_errors(title, body):
    errors = {}

    if not title:
        errors['title'] = 'Please enter a title.'
    if not body:
        errors['body'] = ('Your blog post cannot be blank. Please enter your ' +
                          'blog post content.')

    return errors

def comment_errors(comment):
    errors = {}

    if not comment:
        errors['comment'] = 'Comment cannot be blank.'

    return errors

def editpost_errors(title, body):
    errors = {}

    if not title:
        errors['title'] = 'Title cannot be blank.'
    if not body:
        errors['body'] = 'Your blog post cannot be blank.'

    return errors
