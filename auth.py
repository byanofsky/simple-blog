import hashlib
import hmac
import random
import string
from passlib.hash import pbkdf2_sha256

# TODO: get secret key from config file
SECRET_KEY = 'insert secret key'

def hash_str(s):
    return hmac.new(SECRET_KEY, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split("|")[0]
    if h == make_secure_val(val):
        return val

def make_pw_hash(pw):
    return pbkdf2_sha256.hash(pw)

def verify_pw(pw, hash):
    return pbkdf2_sha256.verify(pw, hash)

# def create_user_cookie(user_key):
#     return make_secure_val(str(user_key.id()))
#
# def check_user_cookie_val(user_cookie_val):
#     if not user_cookie_val:
#         return None
#     return check_scure_val(user_cookie_val)
