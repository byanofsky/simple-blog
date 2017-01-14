from handlers.basehandler import BaseHandler
from modules.validation import get_user, post_exists


class ViewPostHandler(BaseHandler):
    @post_exists
    @get_user
    def get(self, user, post, post_id):
        self.render(
            'viewpost.html',
            user=user,
            post=post,
            post_id=post_id,
            comments=post.get_comments()
        )
