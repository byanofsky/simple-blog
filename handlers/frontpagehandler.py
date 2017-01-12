from google.appengine.datastore.datastore_query import Cursor
from handlers.basehandler import BaseHandler
from models.post import Post


class FrontPageHandler(BaseHandler):
    def get(self):
        # Constant for how many posts to display per page
        POSTS_PER_PAGE = 10
        # TODO: can we move cursor to post? to reduce imports?
        cursor = Cursor(urlsafe=self.request.get('cursor'))
        posts, next_cursor, more = Post.get_n_posts(
            n=POSTS_PER_PAGE,
            cursor=cursor
        )

        # TODO: code for building multi-page frontpage
        # next cursor to ouput to url
        # next_cursor.urlsafe()

        self.render('frontpage.html', posts=posts)
