from tornado.web import RequestHandler


class HotsHandler(RequestHandler):

    async def get_hots(self, redis):
        return [hot.decode() for hot in await redis.zrevrangebyscore('hot', count=5, offset=0)]
