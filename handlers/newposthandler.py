from handlers.basehandler import BaseHandler
from modules.validation import require_user
import modules.form_validation as validate
from models.post import Post


class NewPostHandler(BaseHandler):
    @require_user('login')
    def get(self, user):
        self.render('newpost.html')

    @require_user('login')
    def post(self, user):
        title = self.request.get('title')
        body = self.request.get('body')

        # Validate newpost form
        errors = validate.check_newpost(title, body)

        if errors:
            self.render(
                'newpost.html',
                title=title,
                body=body,
                errors=errors
            )
        else:
            # Create post in database, and redirect to singlepost
            post_key = Post.create(
                title=title,
                body=body,
                author=user
            )
            self.redirect_to('viewpost', post_id=post_key.id())
