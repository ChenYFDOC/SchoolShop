from tornado import web, ioloop
from settings import settings
from urls import url_match

if __name__ == '__main__':
    web.Application([
        *url_match,
    ], **settings).listen(8080)
    ioloop.IOLoop.current().start()
