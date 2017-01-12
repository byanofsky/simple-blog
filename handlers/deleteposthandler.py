from handlers.basehandler import BaseHandler
from modules.validation import user_owns_post


class DeletePostHandler(BaseHandler):
    @user_owns_post
    def get(self, user, post_id, post):
        # make sure user wants to delete. Confirm or cancel
        self.render('deletepost.html', post=post)

    @user_owns_post
    def post(self, user, post_id, post):
        # if confirm, post here
        post.delete()
        self.render('deletepost.html', deleted=True)
