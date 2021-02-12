from .handlers import *
from tornado.web import url

url_match = [
    url(r'/login/?', LoginHandler, name='login'),
    url(r'/login/pic_code/(\d*)/?', PicCode, name='pic_code'),
    url(r'/regist/?', RegistHandler, name='regist'),
    url(r'/regist/phone_message/?', MessageHandler, name='phone_message'),
    url(r'/user_info/?', ProfileHandler, name='profile'),
    url(r'/logout/?', LogoutHandler, name='logout')
]
