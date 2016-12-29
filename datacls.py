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

    # @classmethod
    # def create_post(cls)
    #
class User(ndb.Model):
    username = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = False)
    created = ndb.DateTimeProperty(auto_now_add = True)

    def create_user_cookie(self):
        return make_secure_val(self.key().id())

    # @classmethod
    # def check_user_cookie(cls):
    #     return check_secure_val

    @classmethod
    def by_name(cls):
        return cls.query().order(cls.username)

    @classmethod
    def create(cls, un, pw, email):
        hashed_pw = make_pw_hash(pw)
        u = cls(username=un, password=hashed_pw, email=email )
        return u.put()

    @classmethod
    def exists(cls, un):
        return cls.query(cls.username == un).fetch()
