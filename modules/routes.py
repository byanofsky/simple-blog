import webapp2

from handlers.frontpagehandler import FrontPageHandler
from handlers.signuphandler import SignUpHandler
from handlers.welcomehandler import WelcomeHandler
from handlers.loginhandler import LoginHandler
from handlers.logouthandler import LogoutHandler
from handlers.newposthandler import NewPostHandler
from handlers.viewposthandler import ViewPostHandler
from handlers.editposthandler import EditPostHandler
from handlers.deleteposthandler import DeletePostHandler
from handlers.likeposthandler import LikePostHandler
from handlers.unlikeposthandler import UnlikePostHandler
from handlers.newcommenthandler import NewCommentHandler
from handlers.editcommenthandler import EditCommentHandler
from handlers.deletecommenthandler import DeleteCommentHandler

# TODO: handle routes for just post, deletepost, etc when no post id
route_list = [
    webapp2.Route('/', handler=FrontPageHandler, name='frontpage'),
    webapp2.Route('/signup', handler=SignUpHandler, name='signup'),
    webapp2.Route('/welcome', handler=WelcomeHandler, name='welcome'),
    webapp2.Route('/login', handler=LoginHandler, name='login'),
    webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
    webapp2.Route('/newpost', handler=NewPostHandler, name='newpost'),
    webapp2.Route('/post/<post_id:[0-9]+>', handler=ViewPostHandler,
                  name='viewpost'),
    webapp2.Route('/editpost/<post_id:[0-9]+>', handler=EditPostHandler,
                  name='editpost'),
    webapp2.Route('/deletepost/<post_id:[0-9]+>', handler=DeletePostHandler,
                  name='deletepost'),
    webapp2.Route('/likepost/<post_id:[0-9]+>', handler=LikePostHandler,
                  name='likepost'),
    webapp2.Route('/unlikepost/<post_id:[0-9]+>', handler=UnlikePostHandler,
                  name='unlikepost'),
    webapp2.Route('/newcomment/<post_id:[0-9]+>', handler=NewCommentHandler,
                  name='newcomment'),
    webapp2.Route('/editcomment/<url_comment_key:[a-zA-Z0-9_-]+>',
                  handler=EditCommentHandler,
                  name='editcomment'),
    webapp2.Route('/deletecomment/<url_comment_key:[a-zA-Z0-9_-]+>',
                  handler=DeleteCommentHandler,
                  name='deletecomment')
]
