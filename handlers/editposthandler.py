from handlers.basehandler import BaseHandler
from modules.validation import user_owns_post
import modules.validate


class EditPostHandler(BaseHandler):
    @user_owns_post
    def get(self, user, post_id, post):
        self.render('editpost.html', post=post)

    @user_owns_post
    def post(self, user, post_id, post):
        title = self.request.get('title')
        body = self.request.get('body')

        # Check editpost form for errors
        errors = validate.editpost_errors(title, body)

        if errors:
            msg = ('Your post was not edited.' +
                   'Please fix errors and resubmit.')
            self.render(
                'editpost.html',
                post=post,
                title=title,
                body=body,
                msg=msg,
                errors=errors
            )
        else:
            # No errors, update post
            msg = 'Post successfully updated.'
            post.update(title, body)
            # TODO: should we redirect so user can't go back and post?
            self.render(
                'editpost.html',
                post=post,
                msg=msg
            )
