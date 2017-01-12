from google.appengine.ext import ndb
from comment import Comment
from modules.auth import (make_secure_val, check_secure_val, make_hashed_pw,
                  set_user_cookie)
from modules.validate import valid_email


class User(ndb.Model):
    email = ndb.StringProperty(required=True)
    displayname = ndb.StringProperty()
    hashed_pw = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    # Gets user's displayname. If no displayname, returns email.
    def get_displayname(self):
        return self.displayname or self.email

    def like(self, p):
        # Checks if user can like post, and if so, calls add_like
        if self.can_like_post(p):
            return p.add_like(self)

    def unlike(self, p):
        # Checks if user liked post before removing like
        if self.liked_post(p):
            # TODO: Because liked_post can get index, can we pass that here?
            return p.remove_like(self)

    def liked_post(self, p):
        # TODO: if found, can we return index to save some time in unlike?
        return self.key in p.likes

    # Check if user can like post
    def can_like_post(self, p):
        # Makes sure user is not post author, and that user hasn't already
        # liked the post.
        return self.key != p.author and not self.liked_post(p)

    # Checks if user can edit object. Assumes object has
    # an author property.
    def can_edit(self, obj):
        return self.key == obj.author

    # Checks if user can leave a comment
    def leave_comment(self, comment, p):
        return Comment.create(comment, self, p)

    # Creates a user and returns the db key
    @classmethod
    def create(cls, email, pw, displayname):
        # Hash pw for storage
        hashed_pw = make_hashed_pw(pw)
        u = cls(email=email, hashed_pw=hashed_pw, displayname=displayname)
        return u.put()

    # Get user object by email
    @classmethod
    def get_by_email(cls, email):
        # Checks if email is valid before querying db
        if valid_email(email):
            return cls.query(cls.email == email).get()

    # TODO: these signup functions can be moved to their own file
    # Creates a user and uses db key to set user cookie
    @classmethod
    def signup(cls, page_handler, email, pw, displayname):
        u_key = cls.create(email, pw, displayname)
        set_user_cookie(page_handler, u_key)
