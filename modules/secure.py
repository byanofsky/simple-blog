import hmac

from passlib.hash import pbkdf2_sha256

from config import app_config

# Get secret key from config file
SECRET_KEY = app_config['secret_key']


def make_hashed_pw(pw):
    return pbkdf2_sha256.hash(pw)


def verify_pw(pw, hash):
    return pbkdf2_sha256.verify(pw, hash)


# Hash values, for use with cookies
def hash_str(s):
    return hmac.new(SECRET_KEY, s).hexdigest()


# Creates a seure value to use for cookie value.
# Format: value|hashed_value
def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))


# Input a secure value (value|hashed_value).
# Checks value against hashed_value.
# If match, returns value.
def check_secure_val(h):
    val = h.split("|")[0]
    if h == make_secure_val(val):
        return val
