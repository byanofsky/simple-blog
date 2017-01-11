from handlers.basehandler import BaseHandler
from validation import user_owns_comment


class DeleteCommentHandler(BaseHandler):
    @user_owns_comment
    def get(self, user, comment):
        self.render('deletecomment.html', comment=comment)

    @user_owns_comment
    def post(self, user, comment):
        parent_post_id = comment.key.parent().id()
        comment.delete()
        self.render(
            'deletecomment.html',
            parent_post_id=parent_post_id,
            deleted=True
        )
