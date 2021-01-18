import json

from tornado import web
from servers import es, redis
from utils.authLog import auth_decorator
from common_handler import HotsHandler


class IndexHandler(HotsHandler):
    @auth_decorator
    async def get(self):
        return await self.render(r'display/index.html', user_info=self.user, hots=await self.get_hots(redis))

    @auth_decorator
    async def post(self):
        search = self.get_argument('search', '')
        await redis.zincrby('hot', 1, search)


class SearchHandler(web.RequestHandler):
    async def post(self):
        arg = self.get_argument('text')
        rule = json.dumps({
            "_source": False,
            "suggest": {
                "my_suggestions": {
                    "text": arg,
                    "completion": {
                        "field": "nameSuggester",
                        "size": 5,
                        "skip_duplicates": True
                    }
                }
            }
        })
        res = await es.search(body=rule, index='schoolshop')
        search = []
        for item in res['suggest']['my_suggestions'][0]['options']:
            search.append(item['text'])
        return self.finish({'result': search})
