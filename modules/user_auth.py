import secure

from models.user import User
from modules.form_validation import valid_email


# Check login. Returns errors (if any) and user object (if user exists)
def validate_login(email, pw):
    errors = {}
    user = None
    if not valid_email(email):
        errors['email'] = True
    else:
        user = User.get_by_email(email)
        if not user:
            errors['user'] = True
        else:
            valid_login = secure.verify_pw(pw, user.hashed_pw)
            if not valid_login:
                errors['valid_login'] = True
    return errors, user
