import json
import math

from tornado import web
from servers import es, redis, objects
from utils.authLog import auth_decorator
from common_handler import HotsHandler
from ..shop.models import Goods, Order
from apps.users.models import Users
import peewee


class IndexHandler(HotsHandler):
    """
    搜索主页
    """

    @auth_decorator
    async def get(self):
        return await self.render(r'display/index.html', user_info=self.user,
                                 hots=await self.get_hots(redis))


class DisplayHandler(HotsHandler):
    """
    搜索结果
    """

    @auth_decorator
    async def get(self, page='1'):
        search = self.get_argument('search', '')
        if not search:
            return self.redirect(self.reverse_url(name='index'), permanent=False)
        await redis.zincrby('hot', 1, search)
        res = await es.search(index='goods', body=json.dumps({
            '_source': ['id', 'price', 'publisher', 'name', 'comment', 'inventory', 'edit_time'],
            'query': {
                'multi_match': {
                    'query': search,
                    'type': 'cross_fields',
                    'operator': 'and',
                    'fields': ['name', 'comment']
                }
            },
            'from': (int(page) - 1) * 10,
            'size': 7,
            'highlight': {
                "pre_tags": "<font color='#FF0000'>",
                "post_tags": "</font>",
                "fields": {
                    "comment": {},
                    'name': {}
                }
            }
        }))
        for hit in res['hits']['hits']:
            hit['_source'].update(hit['highlight'])
            hit['_source']['id'] = hit['_id']
        return await self.render(r'display\search_res.html',
                                 hots=await self.get_hots(redis),
                                 user_info=self.user,
                                 res=[hit['_source'] for hit in res['hits']['hits']],
                                 pages=math.ceil(res['hits']['total']['value'] / 7),cur_p=page)


class SearchHandler(web.RequestHandler):
    """
    搜索建议提示
    """

    async def post(self):
        arg = self.get_argument('text')
        rule = json.dumps({
            "_source": False,
            "suggest": {
                "my_suggestions": {
                    "text": arg,
                    "completion": {
                        "field": self.get_argument('suggest'),
                        "size": 5,
                        "skip_duplicates": True
                    }
                }
            }
        })
        res = await es.search(body=rule, index=self.get_argument('index'))
        search = []
        for item in res['suggest']['my_suggestions'][0]['options']:
            search.append(item['text'])
        return await self.finish({'result': search})


class GoodHandler(HotsHandler):
    """
    货物描述和联系卖家
    """

    @auth_decorator
    async def get(self, _id):
        good = await objects.get(Goods, id=_id)
        publisher = await objects.get(Users, id=good.publisher_id)
        return await self.render(r'display\good.html', user_info=self.user, hots=await self.get_hots(redis), good=good,
                                 publisher=publisher)


class BuyHandler(HotsHandler):
    """
    商品购买确认和状态
    """

    @auth_decorator
    async def get(self, _id):
        good = await objects.get(Goods, id=_id)
        if good.inventory <= 0:
            return await self.finish({'code': 401})
        else:
            good.inventory -= 1
            good.status = 1
            await objects.update(good, only=['inventory', 'status'])
            await objects.create(Order, good=good, buyer=self.user.id, seller=good.publisher_id)
            await es.update('goods', _id, body=json.dumps({
                'doc': {
                    'inventory': good.inventory
                }
            }))
            return await self.finish({'code': 200})

    @auth_decorator
    async def delete(self):
        id = self.get_argument('id')
        orders = await objects.prefetch(Order.select().where(Order.id == id), Goods.select())
        orders[0].good.inventory += 1
        await objects.update(orders[0].good, only=['inventory'])
        await objects.delete(orders[0])
        await es.update('goods', orders[0].good_id.hex, body=json.dumps({
            'doc': {
                'inventory': orders[0].good.inventory
            }
        }))
        return await self.finish({'code': 200})
