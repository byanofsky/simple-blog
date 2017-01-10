from handlers.basehandler import BaseHandler


class SinglePostHandler(BaseHandler):
    def initialize(self, request, response):
        super(SinglePostHandler, self).initialize(request, response)
        # Get post_id from route
        self.p_id = int(self.request.route_kwargs['post_id'])
        # Save post object
        self.p = Post.get_by_id(self.p_id)
        # Set post title as page title
        self.page_title = self.p.title

    # TODO: can render post be combined into one function
    # TODO: add comment display, edit, delete logic here
    # Helper for singlepost jinja template
    def render_post(self, **kw):
        self.render('singlepost.html', p=self.p,
                    comments=Comment.get_comments(self.p), **kw)

    # Extends render_post for a logged in user
    def render_post_user(self, **kw):
        self.render_post(
            edit_post_uri=self.get_uri('editpost', post_id=self.p_id),
            uri_for=self.get_uri,
            can_comment=True,
            user=self.u,
            can_edit=self.u.can_edit(self.p),
            can_like=self.u.can_like_post(self.p),
            liked_post=self.u.liked_post(self.p),
            **kw)

    def get(self, post_id):
        # TODO: handle errors if post does not exist
        if self.u:
            self.render_post_user()
        else:
            self.render_post()

    def post(self, post_id):
        # Get query string data for "action"
        action = self.request.get('action')
        # The actions that are currently possible on singlepost
        action_list = ['comment', 'like', 'unlike']
        if self.u and (action in action_list):
            if action == 'comment':
                # Process comment form
                comment = self.request.get('comment')
                errors = validate.comment_errors(comment)
                if errors:
                    self.render_post_user(comment=comment, errors=errors)
                else:
                    self.u.leave_comment(comment, self.p)
                    self.redirect_to('singlepost', post_id=post_id)
            else:
                # If action isn't comment, it must be like or unlike.
                # Uses "else" instead of "elif" so redirect can be used.
                if action == 'like':
                    self.u.like(self.p)
                elif action == 'unlike':
                    self.u.unlike(self.p)
                self.redirect_to('singlepost', post_id=post_id)
        else:
            # If no user or no action, redirect user to post
            self.redirect_to('singlepost', post_id=post_id)
