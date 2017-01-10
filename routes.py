from handlers.basehandler import *

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
