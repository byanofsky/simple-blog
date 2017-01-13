import secure

from models.user import User
from modules.form_validation import valid_email


def validate_login(email, pw):
    user = User.get_by_email(email)
    login_errors = {}
    if not user:
        login_errors['user'] = True
    elif not secure.verify_pw(pw, user.hashed_pw):
        login_errors['wrong_pw'] = True
    return user, login_errors

def user_login(email, pw):
    pass
