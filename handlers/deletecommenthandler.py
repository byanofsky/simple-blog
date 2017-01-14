from handlers.basehandler import BaseHandler
from modules.validation import user_owns_comment


class DeleteCommentHandler(BaseHandler):
    @user_owns_comment
    def get(self, user, comment, comment_key):
        self.render('deletecomment.html', comment=comment)

    @user_owns_comment
    def post(self, user, comment, comment_key):
        parent_post_id = comment.key.parent().id()
        comment.delete()
        self.render(
            'deletecomment.html',
            parent_post_id=parent_post_id,
            deleted=True
        )
