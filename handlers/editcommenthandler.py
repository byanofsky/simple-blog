from handlers.basehandler import BaseHandler
from modules.validation import user_owns_comment
import modules.form_validation as validate


class EditCommentHandler(BaseHandler):
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
