from tornado.web import url, RedirectHandler
from .handlers import *

url_match = [
    url(r'/?', RedirectHandler, ({'url': '/index/'})),
    url(r'/index/?', IndexHandler, name='index'),
    url(r'/_search/?', SearchHandler, name='search')
]
