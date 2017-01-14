from handlers.basehandler import BaseHandler
from modules.validation import user_owns_comment
import modules.form_validation as form_validation


class EditCommentHandler(BaseHandler):
    @user_owns_comment
    def get(self, user, comment, comment_key):
        self.render('editcomment.html', comment=comment)

    @user_owns_comment
    def post(self, user, comment, comment_key):
        comment_body = self.request.get('comment_body')

        # Check editcomment form for errors
        errors = form_validation.check_comment(comment_body)

        if errors:
            self.render(
                'editcomment.html',
                comment=comment,
                comment_body=comment_body,
                errors=errors
            )
        else:
            # TODO: what if not updated?
            comment.update(comment_body)
            # TODO: Redirect user so can't resubmit
            self.render(
                'editcomment.html',
                comment=comment,
                updated=True
            )
