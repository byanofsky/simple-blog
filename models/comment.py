from google.appengine.ext import ndb


class Comment(ndb.Model):
    body = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    author = ndb.KeyProperty(required=True, kind='User')

    def update(self, body):
        self.body = body
        return self.put()

    def delete(self):
        self.key.delete()

    @classmethod
    def create(cls, body, author, p):
        c = cls(body=body, author=author.key, parent=p.key)
        return c.put()

    @classmethod
    def get_comments(cls, p):
        return cls.query(ancestor=p.key).order(-cls.created).fetch()

    # Delete all of post p's comments
    @classmethod
    def delete_post_comments(cls, p):
        query = cls.query(ancestor=p.key).order(-cls.created)
        comments = query.fetch(keys_only=True)
        ndb.delete_multi(comments)
