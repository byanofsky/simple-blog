from auth import make_secure_val, check_secure_val, make_hashed_pw, set_user_cookie
from validate import valid_email
from google.appengine.ext import ndb

# TODO: check other datastore options

class Post(ndb.Model):
    title = ndb.StringProperty(required = True)
    body = ndb.TextProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    # TODO: should author be parent? Will that affect query?
    author = ndb.KeyProperty(required = True, kind = 'User')
    likes = ndb.KeyProperty(repeated=True, kind= 'User')

    def update(self, title, body):
        self.title = title
        self.body = body
        return self.put()

    def delete(self):
        Comment.delete_post_comments(self)
        self.key.delete()

    def add_like(self, u):
        # add user to list of likes. Assume user is not on list
        self.likes.append(u.key)
        return self.put()

    def remove_like(self, u):
        # remove user from list of likes. Assume user is on list
        # TODO: we may be able to get the index if liked to shorten time
        self.likes.remove(u.key)
        return self.put()

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
    def get_n(cls, n, cursor = None):
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
        return c.put()

    @classmethod
    def get_comments(cls, p):
        return cls.query(ancestor=p.key).order(-cls.created).fetch()

    @classmethod
    def delete_post_comments(cls, p):
        comments = cls.query(ancestor=p.key).order(-cls.created).fetch(keys_only=True)
        ndb.delete_multi(comments)

class User(ndb.Model):
    email = ndb.StringProperty(required = True)
    displayname = ndb.StringProperty()
    hashed_pw = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

    # gets displayname, either the user display name or email if none
    def get_displayname(self):
        return self.displayname or self.email

    def like(self, p):
        if self.can_like_post(p):
            return p.add_like(self)

    def unlike(self, p):
        if self.liked_post(p):
            return p.remove_like(self)

    def liked_post(self, p):
        # TODO: if found, can we return index to save some time?
        return self.key in p.likes

    def can_like_post(self, p):
        return self.key != p.author and not self.liked_post(p)

    # TODO: can combine these two functions
    def can_edit_post(self, p):
        return self.key == p.author

    def can_edit_comment(self, c):
        return self.key == c.author

    def leave_comment(self, comment, p):
        return Comment.create(comment, self, p)

    # creates a user and returns the db key
    @classmethod
    def create(cls, email, pw, displayname):
        hashed_pw = make_hashed_pw(pw)
        u = cls(email=email, hashed_pw=hashed_pw, displayname=displayname )
        return u.put()

    # get user object by email
    @classmethod
    def get_by_email(cls, email):
        if valid_email(email):
            return cls.query(cls.email == email).get()

    # TODO: these signup functions can be moved to their own file
    # creates a user and uses db key to set user cookie
    @classmethod
    def signup(cls, page_handler, email, pw, displayname):
        u_key = cls.create(email, pw, displayname)
        set_user_cookie(page_handler, u_key)
