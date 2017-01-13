import re

from auth import valid_login

from models.user import User

PASSWORD_RE = re.compile(r'^.{3,20}$')
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_email(email):
    return EMAIL_RE.match(email)


def user_exists(email):
    return User.get_by_email(email)


def valid_password(pw):
    return PASSWORD_RE.match(pw)


def password_match(pw, verify_pw):
    return pw == verify_pw


def check_signup(email, pw, verify_pw):
    errors = {}

    if not valid_email(email):
        errors['email'] = True
    elif user_exists(email):
        errors['user_exists'] = True

    if not valid_password(pw):
        errors['password'] = True

    if not password_match(pw, verify_pw):
        errors['verify_pw'] = True

    return errors


def check_login(email, pw):
    errors = {}

    if not valid_email(email):
        errors['email'] = True

    if not pw:
        errors['pw'] = True

    return errors


def newpost_errors(title, body):
    errors = {}
    if not title:
        errors['title'] = 'Please enter a title.'
    if not body:
        errors['body'] = ('Your blog post cannot be blank. ' +
                          'Please enter your blog post content.')
    return errors


def comment_errors(comment_body):
    errors = {}
    if not comment_body:
        errors['comment_body'] = 'Comment cannot be blank.'
    return errors


def editpost_errors(title, body):
    errors = {}
    if not title:
        errors['title'] = 'Title cannot be blank.'
    if not body:
        errors['body'] = 'Your blog post cannot be blank.'
    return errors


def editcomment_errors(body):
    errors = {}
    if not body:
        errors['body'] = 'Your comment cannot be blank.'
    return errors
