from auth import make_secure_val, check_secure_val
from google.appengine.ext import ndb
from auth import make_pw_hash

# TODO: check other datastore options

# TODO: Need to associate author to user. Most likely as parent
class Post(ndb.Model):
    subject = ndb.StringProperty(required = True)
    content = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)

class User(ndb.Model):
    email = ndb.StringProperty(required = True)
    displayname = ndb.StringProperty(required = False)
    password = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

    # @classmethod
    # def check_user_cookie(cls):
    #     return check_secure_val

    # @classmethod
    # def by_name(cls):
    #     return cls.query().order(cls.username)

    @classmethod
    def create(cls, email, pw, displayname):
        hashed_pw = make_pw_hash(pw)
        u = cls(email=email, password=hashed_pw, displayname=displayname )
        return u.put()

    @classmethod
    def exists(cls, email):
        return cls.query(cls.email == email).fetch()
