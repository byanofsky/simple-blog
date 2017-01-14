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


def create_user(email, pw, displayname):
    hashed_pw = secure.make_hashed_pw(pw)
    return User.create(email, hashed_pw, displayname)


def validate_signup(email, pw, verify_pw, displayname):
    # Set default
    user_key = None
    # Check for form errors
    # TODO: right now, we check form errors, then if email exists.
    # Should email exist check come first?
    errors = form_validation.check_signup(
        email=email,
        pw=pw,
        verify_pw=verify_pw
    )

    if not errors:
        # If no errors, check if user already exists
        if User.get_by_email(email):
            # If user exists, set error
            errors['user_exists'] = True
        else:
            # User does not already exist, and no errors.
            # Create new user.
            user_key = create_user(email, pw, displayname)

    return errors, user_key
