from handlers.basehandler import BaseHandler
from modules.validation import user_can_unlike_post


class UnlikePostHandler(BaseHandler):
    # TODO: do I need a get?
    # Currently gives a 405 error
    # def get(self, post_id):
    #     print 'get liked'

    @user_can_unlike_post
    def post(self, user, post_id, post):
        user.unlike(post)
        self.redirect_to('viewpost', post_id=post_id)
