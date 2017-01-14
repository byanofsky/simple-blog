from handlers.basehandler import BaseHandler
from modules.validation import user_owns_post


class DeletePostHandler(BaseHandler):
    @user_owns_post
    def get(self, user, post, post_id):
        # make sure user wants to delete. Confirm or cancel
        self.render('deletepost.html', post=post)

    @user_owns_post
    def post(self, user, post, post_id):
        # if confirm, post here
        post.delete()
        self.render('deletepost.html', deleted=True)
