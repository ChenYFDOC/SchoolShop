from tornado import ioloop
import wtforms_json
import peewee_async
import aioredis
from utils.genCodePic import ValidCodeImg
from settings import settings


async def get_redis():
    redis = await aioredis.create_redis_pool('redis://' + settings['redis']['host'] + f':{settings["redis"]["port"]}')
    return redis


db = peewee_async.MySQLDatabase(**settings['mysql'])
wtforms_json.init()
db.set_allow_sync(False)
objects = peewee_async.Manager(db)
coder = ValidCodeImg()
redis = ioloop.IOLoop.current().run_sync(func=get_redis)
