from .handlers import *
from tornado.web import url

url_match = [
    url(r'/upload/?', UploadHandler, name='upload'),
    url(r'/user_info/add_good/?', AddGoodHandler, name='add_good'),
    url(r'/user_info/good_detail/?', GoodDetailHandler, name='good_detail'),
]
