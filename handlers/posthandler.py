from handlers.basehandler import BaseHandler
from validation import (get_user, require_user, post_exists,
                        require_user_or_redirect,
                        user_owns_post)
from models.post import Post
from models.comment import Comment
import validate


class ViewPostHandler(BaseHandler):
    @post_exists
    @get_user
    def get(self, user, post_id, post):
        self.render(
            'singlepost.html',
            user=user,
            post=post,
            comments=post.get_comments()
        )

    @post_exists
    @require_user
    def post(self, user, post_id, post):
        # Get query string data for "action"
        action = self.request.get('action')
        # The actions that are currently possible on singlepost
        if action == 'comment':
            print user
            # Process comment form
            # comment = self.request.get('comment')
            # errors = validate.comment_errors(comment)
            # if errors:
            #     self.render_post_user(comment=comment, errors=errors)
            # else:
            #     self.u.leave_comment(comment, self.p)
            #     self.redirect_to('singlepost', post_id=post_id)
        elif action == 'like':
            self.write('like')
        elif action == 'unlike':
            self.write('unlike')
            # If action isn't comment, it must be like or unlike.
            # Uses "else" instead of "elif" so redirect can be used.
            # if action == 'like':
            #     self.u.like(self.p)
            # elif action == 'unlike':
            #     self.u.unlike(self.p)
        self.redirect_to('singlepost', post_id=post_id)


class EditPostHandler(BaseHandler):
    @user_owns_post
    def get(self, user, post_id, post):
        self.render('editpost.html', post=post)

    @user_owns_post
    def post(self, user, post_id, post):
        title = self.request.get('title')
        body = self.request.get('body')

        # Check editpost form for errors
        errors = validate.editpost_errors(title, body)

        if errors:
            msg = ('Your post was not edited.' +
                   'Please fix errors and resubmit.')
            self.render(
                'editpost.html',
                post=post,
                title=title,
                body=body,
                msg=msg,
                errors=errors
            )
        else:
            # No errors, update post
            msg = 'Post successfully updated.'
            post.update(title, body)
            # TODO: should we redirect so user can't go back and post?
            self.render(
                'editpost.html',
                post=post,
                msg=msg
            )


class DeletePostHandler(BaseHandler):
    @user_owns_post
    def get(self, user, post_id, post):
        # make sure user wants to delete. Confirm or cancel
        # TODO: fix this if we need post_id or not
        self.render('deletepost.html', post=post, post_id=post_id)

    @user_owns_post
    def post(self, user, post_id, post):
        # if confirm, post here
        # TODO: fix this. does it pass post or what?
        deleted = post.delete()
        print deleted
        self.render('deletepost.html', deleted=deleted, post=post)
