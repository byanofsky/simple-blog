from handlers.basehandler import BaseHandler
from modules.validation import require_user, post_exists
import modules.validate


class NewCommentHandler(BaseHandler):
    # TODO: do I need a get request handelr?
    def get(self):
        pass

    @post_exists
    @require_user
    def post(self, user, post_id, post):
        # TODO: should this be comment_body or comment?
        comment_body = self.request.get('comment_body')
        errors = validate.comment_errors(comment_body)
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
