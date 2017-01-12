from handlers.basehandler import BaseHandler
from modules.validation import require_user
import modules.validate
from models.post import Post


class NewPostHandler(BaseHandler):
    @require_user
    def get(self, user):
        self.render('newpost.html')

    @require_user
    def post(self, user):
        title = self.request.get('title')
        body = self.request.get('body')
        # Validate newpost form
        errors = validate.newpost_errors(title, body)

        if errors:
            self.render(
                'newpost.html',
                title=title,
                body=body,
                errors=errors
            )
        else:
            # Create post in database, and redirect to singlepost
            post_key = Post.create(title, body, user)
            self.redirect_to('viewpost', post_id=post_key.id())
