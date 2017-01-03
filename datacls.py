from auth import make_secure_val, check_secure_val, make_hashed_pw, set_user_cookie
from google.appengine.ext import ndb

# TODO: check other datastore options

class Post(ndb.Model):
    title = ndb.StringProperty(required = True)
    body = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    author = ndb.KeyProperty(required = True, kind = 'User')

    def update(self, title, body):
        self.title = title
        self.body = body
        return self.put()

    # TODO: should this be part of handler?
    # used on frontpage template
    def get_uri(self, uri_handler):
        return uri_handler('singlepost', post_id=self.key.id())

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
        return self.displayname or self.email

    @classmethod
    def create(cls, email, pw, displayname):
        hashed_pw = make_hashed_pw(pw)
        u = cls(email=email, hashed_pw=hashed_pw, displayname=displayname )
        return u.put()

    @classmethod
    def signup(cls, handler, email, pw, displayname):
        u_key = cls.create(email, pw, displayname)
        set_user_cookie(handler, u_key)

    @classmethod
    def get_by_email(cls, email):
        return cls.query(cls.email == email).get()
