from auth import make_secure_val, check_secure_val
from google.appengine.ext import ndb
from auth import make_pw_hash, set_user_cookie

# TODO: check other datastore options

# TODO: Need to associate author to user. Most likely as parent
class Post(ndb.Model):
    title = ndb.StringProperty(required = True)
    body = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    author = ndb.KeyProperty(required = True, kind = 'User')

    # def set_url(self, base_url):
    #     self.url = base_url + self.key.id()

    # def getx(self):
    #     return self._x
    #
    # def setx(self, value):
    #     self._x = value
    #
    # def delx(self):
    #     del self._x

    def get_url(self, url_handler):
        return url_handler('singlepost', post_id=self.key.id())

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
    hashed_pw = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

    def get_displayname(self):
        # u = ndb.Key(cls, int(u_id)).get()
        return self.displayname or self.email

    @classmethod
    def get_pw_hash(cls, email):
        u = cls.get_by_email(email)
        return u.hashed_pw

    # @classmethod
    # def check_user_cookie(cls):
    #     return check_secure_val

    # @classmethod
    # def by_name(cls):
    #     return cls.query().order(cls.username)

    @classmethod
    def create(cls, email, pw, displayname):
        hashed_pw = make_pw_hash(pw)
        u = cls(email=email, hashed_pw=hashed_pw, displayname=displayname )
        return u.put()

    @classmethod
    def signup(cls, handler, email, pw, displayname):
        u_key = cls.create(email, pw, displayname)
        set_user_cookie(handler, u_key)

    @classmethod
    def get_by_email(cls, email):
        return cls.query(cls.email == email).get()
