from handlers.basehandler import BaseHandler
from modules.validation import user_can_like_post


class LikePostHandler(BaseHandler):
    # # TODO: do I need a get?
    # def get(self, post_id):
    #     print 'get liked'

    @user_can_like_post
    def post(self, user, post_id, post):
        user.like(post)
        self.redirect_to('viewpost', post_id=post_id)
