from auth import make_secure_val, check_secure_val, make_hashed_pw, set_user_cookie
from google.appengine.ext import ndb

# TODO: check other datastore options

class Post(ndb.Model):
    title = ndb.StringProperty(required = True)
    body = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    author = ndb.KeyProperty(required = True, kind = 'User')
    likes = ndb.KeyProperty(repeated=True, kind= 'User')

    def update(self, title, body):
        self.title = title
        self.body = body
        return self.put()

    def add_comment(self, comment_key):
        if not comment_key in self.comments:
            self.comments.append(comment_key)
            self.put()

    # TODO: should this be part of handler?
    # used on frontpage template
    def get_uri(self, uri_handler):
        return uri_handler('singlepost', post_id=self.key.id())

    def add_like(self, u):
        # add user to list of likes. Assume user is not on list
        self.likes.append(u.key)
        self.put()

    def remove_like(self, u):
        # remove user from list of likes. Assume user is on list
        # TODO: we may be able to get the index if liked to shorten time
        self.likes.remove(u.key)
        self.put()

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

    @classmethod
    def get_n(cls, n, cursor):
        return cls.query().order(-cls.created).fetch_page(n, start_cursor=cursor)

class Comment(ndb.Model):
    body = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    author = ndb.KeyProperty(required = True, kind = 'User')

    @classmethod
    def create(cls, body, author, p):
        c = cls(
            body=body,
            author=author.key,
            parent=p.key
        )
        c_key = c.put()

    @classmethod
    def get_comments(cls, p):
        return cls.query(ancestor=p.key).order(-cls.created).fetch()

class User(ndb.Model):
    email = ndb.StringProperty(required = True)
    displayname = ndb.StringProperty(required = False)
    hashed_pw = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

    # gets displayname, either the user display name or email if none
    def get_displayname(self):
        return self.displayname or self.email

    def like(self, p):
        if self.can_like_post(p):
            p.add_like(self)

    def unlike(self, p):
        if self.liked_post(p):
            p.remove_like(self)

    def liked_post(self, p):
        # TODO: if found, can we return index to save some time?
        return self.key in p.likes

    def can_edit_post(self, p):
        return self.key == p.author

    def can_like_post(self, p):
        return self.key != p.author and not self.liked_post(p)

    # creates a user and returns the db key
    @classmethod
    def create(cls, email, pw, displayname):
        hashed_pw = make_hashed_pw(pw)
        u = cls(email=email, hashed_pw=hashed_pw, displayname=displayname )
        return u.put()

    # creates a user and uses db key to set user cookie
    @classmethod
    def signup(cls, page_handler, email, pw, displayname):
        u_key = cls.create(email, pw, displayname)
        set_user_cookie(page_handler, u_key)

    # get user object by email
    @classmethod
    def get_by_email(cls, email):
        return cls.query(cls.email == email).get()
