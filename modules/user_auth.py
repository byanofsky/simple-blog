import secure

from models.user import User
import modules.form_validation as form_validation


# Takes an email and pw from login form,
# and returns any errors and user object
def validate_login(email, pw):
    # Set default to no user
    user = None
    # Check for form errors (if email and pw entered)
    errors = form_validation.check_login(email, pw)

    if not errors:
        # If no errors, check if user exists
        user = User.get_by_email(email)
        if not user:
            # If user does not exist, set error.
            errors['user'] = True
        else:
            # If user exists, check if pw is correct
            valid_login = secure.verify_pw(pw, user.hashed_pw)
            if not valid_login:
                # If password isn't correct, set error
                errors['login'] = True

    return errors, user
