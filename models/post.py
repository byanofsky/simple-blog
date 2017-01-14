from google.appengine.ext import ndb

from comment import Comment


class Post(ndb.Model):
    title = ndb.StringProperty(required=True)
    body = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    # TODO: should author be parent? Will that affect query?
    author = ndb.KeyProperty(required=True, kind='User')
    likes = ndb.KeyProperty(repeated=True, kind='User')

    def update(self, title, body):
        self.title = title
        self.body = body
        return self.put()

    def delete(self):
        Comment.delete_post_comments(self)
        self.key.delete()

    def add_like(self, user):
        # Add user to list of likes. Assumes user is not on list, or will add
        # a duplicate entry.
        self.likes.append(user.key)
        return self.put()

    def remove_like(self, user):
        # Remove user from list of likes. Assumes user is on list.
        self.likes.remove(user.key)
        return self.put()

    def get_comments(self):
        return Comment.get_comments(self)

    # Creates a post. Author assumed to be user object.
    @classmethod
    def create(cls, title, body, author):
        post = cls(title=title, body=body, author=author.key)
        return post.put()

    @classmethod
    def get_all_posts(cls):
        return cls.query().order(-cls.created).fetch()

    @classmethod
    def get_n_posts(cls, n, cursor=None):
        query = cls.query().order(-cls.created)
        return query.fetch_page(n, start_cursor=cursor)
