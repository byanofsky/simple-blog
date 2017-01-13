from handlers.basehandler import BaseHandler
from modules.validation import require_user, post_exists
import modules.form_validation as form_validation


class NewCommentHandler(BaseHandler):
    @post_exists
    @require_user()
    def get(self, user, post, post_id):
        self.render(
            'newcomment.html',
            post_id=post_id
        )

    @post_exists
    @require_user()
    def post(self, user, post, post_id):
        comment_body = self.request.get('comment_body')

        errors = form_validation.check_comment(comment_body)

        if errors:
            # TODO: may be able to combine editcomment and new comment
            self.render(
                'newcomment.html',
                comment_body=comment_body,
                post_id=post_id,
                errors=errors
            )
        else:
            user.leave_comment(comment_body, post)
            self.redirect_to('viewpost', post_id=post_id)
