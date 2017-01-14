from handlers.basehandler import BaseHandler
from modules.validation import user_can_unlike_post


class UnlikePostHandler(BaseHandler):
    # TODO: do I need a get?
    # def get(self, post_id):
    #     print 'get liked'

    @user_can_unlike_post
    def post(self, user, post, post_id):
        user.unlike(post)
        self.redirect_to('viewpost', post_id=post_id)
