from auth import make_secure_val, check_secure_val
from google.appengine.ext import ndb

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
    def create_user(cls, un, pw, email):
        u = cls(username=un, password=pw, email=email )
        return u


# new_id = ndb.Model.allocate_ids(size=1)[0]
# print "ID: " + str(new_id)
