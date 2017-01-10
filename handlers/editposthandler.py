from handlers.basehandler import BaseHandler


class EditPostHandler(BaseHandler):
    # TODO: need to finetune this
    page_title = 'Edit Post'

    def initialize(self, request, response):
        super(EditPostHandler, self).initialize(request, response)
        # initialize post object
        self.p = Post.get_by_id(int(self.request.get('post_id')))

    # TODO: need a render post function
    def render_edit_page(self, **kw):
        # TODO: this may be bad since it is getting post id again for post_uri
        self.render('editpost.html', p=self.p,
                    post_uri=self.get_post_uri(self.p), **kw)

    def get(self):
        # Check if logged in user can edit this post
        if self.u and self.u.can_edit(self.p):
            self.render_edit_page()
        else:
            self.error_redirect('editpost')

    def post(self):
        # Check if logged in user can edit this post
        if self.u and self.u.can_edit(self.p):
            # TODO: are there are any issues here with security
            # (if someone deletes anothers post)
            action = self.request.get('action')
            if action == 'delete':
                self.p.delete()
                self.success_redirect('postdelete')
            # TODO: need an edit action here
            # If action isn't delete, then it is to edit post
            else:
                # User used editpost form
                title = self.request.get('title')
                body = self.request.get('body')
                # Check editpost form for errors
                errors = validate.editpost_errors(title, body)

                if errors:
                    msg = ('Your post was not edited.' +
                           'Please fix errors and resubmit.')
                    self.render_edit_page(title=title, body=body, msg=msg,
                                          errors=errors)
                else:
                    # No errors, update post
                    msg = 'Post successfully updated.'
                    self.p.update(title, body)
                    # TODO: should we redirect so user can't go back and post?
                    self.render_edit_page(msg=msg)
        else:
            # If no user logged in, redirect to error page
            self.error_redirect('editpost')
