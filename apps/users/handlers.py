from tornado import web


class LoginHandler(web.RequestHandler):
    async def get(self, *args, **kwargs):
        await self.render('users\login.html')


class PicCode(web.RequestHandler):

    def initialize(self, redis, coder, *args, **kwargs):
        self.redis = redis
        self.coder = coder

    async def get(self, *args, **kwargs):
        f, code = self.coder.getValidCodeImg()
        await self.redis.set(code, code, expire=30)
        self.set_header("Content-Type", "image/png")
        await self.finish(f.getvalue())
