from tornado.web import url, RedirectHandler
from .handlers import *

url_match = [
    url(r'/?', RedirectHandler, ({'url': '/index/'})),
    url(r'/index/?', IndexHandler, name='index'),
    url(r'/index/(\d*)/?', DisplayHandler, name='display'),
    url(r'/_search/?', SearchHandler, name='search'),
    url(r'/good/(\w*)/?', GoodHandler, name='good'),
    url(r'/good/(\w*)/buy/?', BuyHandler, name='buy'),
    url(r'/good/order/delete/?', BuyHandler, name='del_o')
]
