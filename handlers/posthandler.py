from handlers.basehandler import BaseHandler
from validation import get_user, require_user, post_exists
from models.post import Post
from models.comment import Comment


class ViewPostHandler(BaseHandler):
    @post_exists
    @get_user
    def get(self, user, post_id, post):
        self.render(
            'singlepost.html',
            user=user,
            post=post,
            comments=post.get_comments()
        )

    @post_exists
    @require_user
    def post(self, user, post_id, post):
        # Get query string data for "action"
        action = self.request.get('action')
        # The actions that are currently possible on singlepost
        if action == 'comment':
            print user
            # Process comment form
            # comment = self.request.get('comment')
            # errors = validate.comment_errors(comment)
            # if errors:
            #     self.render_post_user(comment=comment, errors=errors)
            # else:
            #     self.u.leave_comment(comment, self.p)
            #     self.redirect_to('singlepost', post_id=post_id)
        elif action == 'like':
            self.write('like')
        elif action == 'unlike':
            self.write('unlike')
            # If action isn't comment, it must be like or unlike.
            # Uses "else" instead of "elif" so redirect can be used.
            # if action == 'like':
            #     self.u.like(self.p)
            # elif action == 'unlike':
            #     self.u.unlike(self.p)
        self.redirect_to('singlepost', post_id=post_id)
