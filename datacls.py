from auth import make_secure_val, check_secure_val
from google.appengine.ext import ndb
from auth import make_pw_hash

# TODO: check other datastore options

# TODO: Need to associate author to user. Most likely as parent
class Post(ndb.Model):
    title = ndb.StringProperty(required = True)
    body = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    author = ndb.KeyProperty(required = True, kind = 'User')

    @classmethod
    def create(cls, title, body, author):
        p = cls(
            title=title,
            body=body,
            author=author.key
        )
        return p.put()

    @classmethod
    def get_all(cls):
        return cls.query().order(-cls.created).fetch()

class User(ndb.Model):
    email = ndb.StringProperty(required = True)
    displayname = ndb.StringProperty(required = False)
    password = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

    @classmethod
    def get_display_name(cls, u_id):
        u = ndb.Key(cls, int(u_id)).get()
        return u.displayname or u.email

    @classmethod
    def get_pw_hash(cls, email):
        u = cls.get_by_email(email)
        return u.password

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

    @classmethod
    def get_by_email(cls, email):
        # return cls.exists(email)[0]
        print cls.query(cls.email == email)
        return cls.query(cls.email == email).get()
