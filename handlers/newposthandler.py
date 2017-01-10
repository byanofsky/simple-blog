from handlers.basehandler import BaseHandler


class NewPostHandler(BaseHandler):
    page_title = 'New Post'

    def get(self):
        if self.u:
            self.render('newpost.html')
        else:
            self.error_redirect('createpost')

    def post(self):
        if self.u:
            title = self.request.get('title')
            body = self.request.get('body')
            # Validate newpost form
            errors = validate.newpost_errors(title, body)

            if errors:
                self.render('newpost.html', title=title, body=body,
                            errors=errors)
            else:
                # Create post in database, and redirect to singlepost
                p_key = Post.create(title, body, self.u)
                self.redirect_to('singlepost', post_id=p_key.id())
        else:
            # If no user logged in, redirect to error page
            self.error_redirect('createpost')
