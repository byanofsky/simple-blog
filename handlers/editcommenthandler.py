from handlers.basehandler import BaseHandler


class EditCommentHandler(BaseHandler):
    # TODO: need to finetune this like edit post
    # TODO: can combine with editpost?
    page_title = 'Edit Comment'

    def initialize(self, request, response):
        super(EditCommentHandler, self).initialize(request, response)
        # Initialize comment object
        # TODO: fix this up
        c_key = ndb.Key(urlsafe=self.request.get('comment_key'))
        self.c = c_key.get()
        # Initialize post object from comment parent
        self.p = c_key.parent().get()

    def render_edit_page(self, **kw):
        # TODO: this may be bad since it is getting post id again
        # TODO: need to get parent post url
        self.render('editcomment.html', c=self.c,
                    post_uri=self.get_post_uri(self.p), **kw)

    def get(self):
        # Check if user can edit comment
        if self.u and self.u.can_edit(self.c):
            self.render_edit_page()
        else:
            # If user can't edit comment, redirect to error page
            self.error_redirect('editcomment', post=self.p.key.urlsafe())

    def post(self):
        if self.u and self.u.can_edit(self.c):
            # TODO: are there are any issues here with security.
            # Such as if someone deletes anothers post.

            # Check user's action
            action = self.request.get('action')
            if action == 'delete':
                self.c.delete()
                self.success_redirect('commentdelete',
                                      post=self.p.key.urlsafe())
            elif action == 'update':
                body = self.request.get('body')
                # Check editcomment form for errors
                errors = validate.editcomment_errors(body)
                if errors:
                    msg = ('Your comment was not edited.' +
                           'Please fix errors and resubmit.')
                    self.render_edit_page(body=body, msg=msg, errors=errors)
                else:
                    # TODO: what if not updated?
                    self.c.update(body)
                    msg = 'Comment successfully updated.'
                    self.render_edit_page(msg=msg)
            else:
                # If action is not delete or update
                msg = 'No changes made.'
                self.render_edit_page(msg=msg)
        else:
            # If no user logged in or user can't edit comment,
            # redirect to error page
            self.error_redirect('editcomment', post=self.p.key.urlsafe())
