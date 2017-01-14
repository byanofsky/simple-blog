import re


PASSWORD_RE = re.compile(r'^.{3,20}$')
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_email(email):
    return EMAIL_RE.match(email)


def valid_password(pw):
    return PASSWORD_RE.match(pw)


def password_match(pw, verify_pw):
    return pw == verify_pw


def check_signup(email, pw, verify_pw):
    errors = {}

    if not valid_email(email):
        errors['email'] = True

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


def check_newpost(title, body):
    errors = {}

    if not title:
        errors['title'] = True

    if not body:
        errors['body'] = True

    return errors


def check_comment(comment_body):
    errors = {}

    if not comment_body:
        errors['comment_body'] = True

    return errors


def editpost_errors(title, body):
    errors = {}
    if not title:
        errors['title'] = 'Title cannot be blank.'
    if not body:
        errors['body'] = 'Your blog post cannot be blank.'
    return errors
