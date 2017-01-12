import hmac

from passlib.hash import pbkdf2_sha256

from config import app_config

# Get secret key from config file
SECRET_KEY = app_config['secret_key']


def make_hashed_pw(pw):
    return pbkdf2_sha256.hash(pw)


def verify_pw(pw, hash):
    return pbkdf2_sha256.verify(pw, hash)


def valid_login(u, pw):
    return verify_pw(pw, u.hashed_pw)


def hash_str(s):
    return hmac.new(SECRET_KEY, s).hexdigest()


def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    val = h.split("|")[0]
    if h == make_secure_val(val):
        return val


# TODO: perhaps move these to a file for logging in and out
def get_user_cookie(handler):
    return handler.request.cookies.get('user_id')


def get_user_cookie_id(handler):
    u_cookie = get_user_cookie(handler)
    if u_cookie:
        return check_secure_val(u_cookie)


def set_user_cookie(handler, u_key):
    u_cookie = make_secure_val(str(u_key.id()))
    handler.response.set_cookie('user_id', u_cookie)


def clear_user_cookie(handler):
    handler.response.set_cookie('user_id', None)
