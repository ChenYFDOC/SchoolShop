from tornado import ioloop
import wtforms_json
import peewee_async
import aioredis
from utils.genCodePic import ValidCodeImg
from settings import settings
from elasticsearch import AsyncElasticsearch
from functools import partial

'''
创建各式微服务
'''
es = AsyncElasticsearch(hosts=settings['es']['host'])
db = peewee_async.PooledMySQLDatabase(**settings['mysql'])
wtforms_json.init()
db.set_allow_sync(False)
objects = peewee_async.Manager(db)
coder = ValidCodeImg()
redis = ioloop.IOLoop.current().run_sync(
    func=partial(aioredis.create_redis_pool, 'redis://' + settings['redis']['host'] + f':{settings["redis"]["port"]}'))
