from .handlers import *
from settings import settings
from tornado import ioloop
from utils.genCodePic import ValidCodeImg
import aioredis


async def get_redis():
    redis = await aioredis.create_redis_pool('redis://' + settings['redis']['host'] + f':{settings["redis"]["port"]}')
    return redis


redis = ioloop.IOLoop.current().run_sync(func=get_redis)
url_match = [
    (r'/login/', LoginHandler),
    (r'/login/pic_code/', PicCode, {'redis': redis, 'coder': ValidCodeImg()})
]
