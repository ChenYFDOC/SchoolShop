from tornado import web, ioloop
from settings import settings
from urls import url_match

if __name__ == '__main__':
    app = web.Application([
        *url_match,
        (r'/media/(.*)', web.StaticFileHandler, {'path': settings['media_path']}, 'media')
    ], **settings)
    app.listen(8080)
    ioloop.IOLoop.current().start()
