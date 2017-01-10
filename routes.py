import webapp2

from handlers.frontpagehandler import FrontPageHandler
from handlers.signuphandler import SignUpHandler
from handlers.welcomehandler import WelcomeHandler
from handlers.loginhandler import LoginHandler
from handlers.logouthandler import LogoutHandler
from handlers.newposthandler import NewPostHandler
from handlers.singleposthandler import SinglePostHandler
from handlers.editposthandler import EditPostHandler
from handlers.editcommenthandler import EditCommentHandler
from handlers.errorhandler import ErrorHandler
from handlers.successhandler import SuccessHandler

route_list = [
    webapp2.Route('/', handler=FrontPageHandler, name='frontpage'),
    webapp2.Route('/signup', handler=SignUpHandler, name='signup'),
    webapp2.Route('/welcome', handler=WelcomeHandler, name='welcome'),
    webapp2.Route('/login', handler=LoginHandler, name='login'),
    webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
    webapp2.Route('/newpost', handler=NewPostHandler, name='newpost'),
    webapp2.Route('/post/<post_id:[0-9]+>', handler=SinglePostHandler,
                  name='singlepost'),
    webapp2.Route('/editpost', handler=EditPostHandler, name='editpost'),
    webapp2.Route('/editcomment', handler=EditCommentHandler,
                  name='editcomment'),
    webapp2.Route('/error', handler=ErrorHandler, name='error'),
    webapp2.Route('/success', handler=SuccessHandler, name='success')
]
