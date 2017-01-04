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
    comments = ndb.KeyProperty(repeated=True, kind= 'Comment')

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

    def add_like(self, u_key):
        # add user to list of likes. Assumes user not in list
        if not u_key in self.likes:
            self.likes.append(u_key)
            self.put()

    def remove_like(self, u_key):
        if u_key in self.likes:
            self.likes.remove(u_key)
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

class Comment(ndb.Model):
    body = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    author = ndb.KeyProperty(required = True, kind = 'User')
    post = ndb.KeyProperty(required = True, kind = 'Post')

    @classmethod
    def create(cls, body, author, p):
        c = cls(
            body=body,
            author=author.key,
            post=p.key
        )
        c_key = c.put()
        p.add_comment(c_key)

    # @classmethod
    # def get_post_comments(cls, p):
    #     comments = []
    #     comments = p.comments
    #     for

class User(ndb.Model):
    email = ndb.StringProperty(required = True)
    displayname = ndb.StringProperty(required = False)
    hashed_pw = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

    def get_displayname(self):
        return self.displayname or self.email

    def like(self, p):
        if not self.key == p.author:
            p.add_like(self.key)

    def liked_post(self, p):
        return self.key in p.likes

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
