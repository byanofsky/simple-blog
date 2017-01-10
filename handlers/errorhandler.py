from handlers.basehandler import BaseHandler


# TODO: combine error and success
# This handles errors, such as when visitor tries to edit
# someone else's posts.
class ErrorHandler(BaseHandler):
    page_title = 'Error'

    def get(self):
        # Get error code passed
        code = self.request.get('code')
        if code == 'editpost':
            error_msg = 'You cannot edit this post.'
            back_url = self.uri_for('frontpage')
            back_text = 'Go to homepage.'
        elif code == 'editcomment' and self.request.get('post'):
            # Get post key passed to allow redirect back to post
            p_key = ndb.Key(urlsafe=self.request.get('post'))
            error_msg = 'You cannot edit this comment.'
            back_url = self.uri_for('singlepost', post_id=p_key.id())
            back_text = 'Go back to post.'
        elif code == 'createpost':
            error_msg = 'You must be logged in to create a post.'
            back_url = self.uri_for('login')
            back_text = 'Login.'
        else:
            error_msg = 'There was an error.'
            back_url = self.uri_for('frontpage')
            back_text = 'Go to homepage.'
        self.render('notice.html', msg=error_msg, url=back_url, text=back_text)
