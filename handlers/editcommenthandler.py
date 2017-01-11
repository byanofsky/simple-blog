from handlers.basehandler import BaseHandler
from validation import user_owns_comment
from validation import comment_exists
from validation import require_user
import validate


class EditCommentHandler(BaseHandler):
    # TODO: need to finetune this like edit post
    # TODO: can combine with editpost?
    # def initialize(self, request, response):
    #     super(EditCommentHandler, self).initialize(request, response)
    #     # Initialize comment object
    #     # TODO: fix this up
    #     c_key = ndb.Key(urlsafe=self.request.get('comment_key'))
    #     self.c = c_key.get()
    #     # Initialize post object from comment parent
    #     self.p = c_key.parent().get()

    # def render_edit_page(self, **kw):
    #     # TODO: this may be bad since it is getting post id again
    #     # TODO: need to get parent post url
    #     self.render('editcomment.html', c=self.c,
    #                 post_uri=self.get_post_uri(self.p), **kw)

    @user_owns_comment
    def get(self, user, comment):
        self.render('editcomment.html', comment=comment)

    @user_owns_comment
    def post(self, user, comment):
        body = self.request.get('body')

        # Check editcomment form for errors
        errors = validate.editcomment_errors(body)

        if errors:
            msg = ('Your comment was not edited.' +
                   'Please fix errors and resubmit.')
            self.render(
                'editcomment.html',
                comment=comment,
                body=body,
                msg=msg,
                errors=errors
            )
        else:
            # TODO: what if not updated?
            comment.update(body)
            msg = 'Comment successfully updated.'
            # TODO: should user get redirected to prevent resubmitting?
            self.render(
                'editcomment.html',
                comment=comment,
                msg=msg
            )
        #
        #     # Check user's action
        #     action = self.request.get('action')
        #     if action == 'delete':
        #         self.c.delete()
        #         self.success_redirect('commentdelete',
        #                               post=self.p.key.urlsafe())
        #     elif action == 'update':
        #         body = self.request.get('body')
        #         # Check editcomment form for errors
        #         errors = validate.editcomment_errors(body)
        #         if errors:
        #             msg = ('Your comment was not edited.' +
        #                    'Please fix errors and resubmit.')
        #             self.render_edit_page(body=body, msg=msg, errors=errors)
        #         else:
        #             # TODO: what if not updated?
        #             self.c.update(body)
        #             msg = 'Comment successfully updated.'
        #             self.render_edit_page(msg=msg)
        #     else:
        #         # If action is not delete or update
        #         msg = 'No changes made.'
        #         self.render_edit_page(msg=msg)
        # else:
        #     # If no user logged in or user can't edit comment,
        #     # redirect to error page
        #     self.error_redirect('editcomment', post=self.p.key.urlsafe())
