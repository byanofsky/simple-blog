from handlers.basehandler import BaseHandler
from modules.validation import user_owns_post
import modules.form_validation as form_validation


class EditPostHandler(BaseHandler):
    @user_owns_post
    def get(self, user, post, post_id):
        self.render('editpost.html', post=post)

    @user_owns_post
    def post(self, user, post, post_id):
        title = self.request.get('title')
        body = self.request.get('body')

        # Check editpost form for errors
        errors = form_validation.check_post(title, body)

        if errors:
            self.render(
                'editpost.html',
                post=post,
                title=title,
                body=body,
                errors=errors
            )
        else:
            # No errors, update post
            post.update(title, body)
            # TODO: should we redirect so user can't go back and post?
            self.render(
                'editpost.html',
                post=post,
                updated=True
            )
