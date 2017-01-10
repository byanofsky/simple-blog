from handlers.basehandler import BaseHandler


# This handles success messages, such as after deleting a comment
class SuccessHandler(BaseHandler):
    page_title = 'Success'

    def get(self):
        # Get success code
        code = self.request.get('code')
        if code == 'postdelete':
            success_msg = 'Post deleted.'
            next_url = self.uri_for('frontpage')
            next_text = 'Go to homepage'
        elif code == 'commentdelete' and self.request.get('post'):
            # Get post key to allow return to post
            p_key = ndb.Key(urlsafe=self.request.get('post'))
            success_msg = 'Comment deleted.'
            next_url = self.uri_for('singlepost', post_id=p_key.id())
            next_text = 'Back to post'
        else:
            success_msg = 'Action completed successfully.'
            next_url = self.uri_for('frontpage')
            next_text = 'Go to homepage'
        self.render('notice.html', msg=success_msg, url=next_url,
                    text=next_text)
