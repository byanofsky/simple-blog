import hashlib
import hmac
import random
import string

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
