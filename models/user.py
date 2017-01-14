from google.appengine.ext import ndb
from comment import Comment
# TODO: I want to remove auth here
from modules.auth import (make_secure_val, check_secure_val, make_hashed_pw,
                  set_user_cookie)


class User(ndb.Model):
    email = ndb.StringProperty(required=True)
    displayname = ndb.StringProperty()
    hashed_pw = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    # Gets user's displayname. If no displayname, returns email.
    def get_displayname(self):
        return self.displayname or self.email

    def like(self, post):
        # Checks if user can like post, and if so, calls add_like
        if self.can_like_post(post):
            return post.add_like(self)

    def unlike(self, post):
        # Checks if user liked post before removing like
        if self.liked_post(post):
            # TODO: Because liked_post can get index, can we pass that here?
            return post.remove_like(self)

    def liked_post(self, post):
        # TODO: if found, can we return index to save some time in unlike?
        return self.key in post.likes

    # Check if user can like post
    def can_like_post(self, post):
        # Makes sure user is not post author, and that user hasn't already
        # liked the post.
        return self.key != post.author and not self.liked_post(post)

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
        u = cls(
            email=email,
            hashed_pw=hashed_pw,
            displayname=displayname
        )
        return u.put()

    # Get user object by email
    @classmethod
    def get_by_email(cls, email):
        return cls.query(cls.email == email).get()
