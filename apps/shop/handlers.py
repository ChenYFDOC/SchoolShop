import json

import aiofiles
from tornado import web
from utils.authLog import auth_decorator
from hashlib import md5
from settings import settings
from .forms import *
from .models import *
from servers import objects, es


class UploadHandler(web.RequestHandler):
    """
    处理上传的商品描述图片和视频
    """

    @auth_decorator
    async def post(self):
        for k, v in self.request.files.items():
            hash_name = md5((img_name := k.split('.'))[0].encode()).hexdigest()
            if v[0]['content_type'].startswith('image'):
                data = []
                async with aiofiles.open(
                        settings['media_path'] + 'goods/image/' + (
                                res_name := (hash_name + '_' + self.user.id.hex + '.' + img_name[-1])),
                        mode='wb') as img:
                    await img.write(v[0]['body'])
                data.append('/media/goods/image/' + res_name)
            if v[0]['content_type'].startswith('video'):
                data = {}
                async with aiofiles.open(
                        settings['media_path'] + 'goods/video/' + (
                                res_name := (hash_name + '_' + self.user.id.hex + '.' + img_name[-1])),
                        mode='wb') as img:
                    await img.write(v[0]['body'])
                data['url'] = '/media/goods/video/' + res_name
        await self.finish({'errno': 0, 'data': data})


class AddGoodHandler(web.RequestHandler):
    """
    发布新货物接口
    """

    @auth_decorator
    async def post(self):
        good_form = Good(self.request.arguments)
        if good_form.validate():
            if good_id := self.get_argument('good_id', ''):
                await objects.execute(Goods.update(**good_form.data).where(Goods.id == good_id))
            else:
                good = await objects.create(Goods, publisher=self.user, **good_form.data)
                good_id = good.id.hex
            del good_form.description
            await es.index(index='goods', id=good_id, body=json.dumps({
                **good_form.data,
                'publisher': self.user.id.hex,
                'status': 0,
                'edit_time': datetime.now().date().isoformat(),
                'suggest': {
                    'input': good_form.data['name']
                }
            }))
            return await self.finish({'status': 200})

        else:
            reason = {}
            for field in good_form.errors:
                reason[field] = good_form.errors[field][0]
            return await self.finish({'status': 400, 'reason': reason})

    @auth_decorator
    async def delete(self):
        good_id = self.get_argument('good_id', '', strip=True)
        res = await objects.execute(Goods.delete().where(Goods.id == good_id))
        await es.delete(index='goods', id=good_id)
        return await self.finish({'status': 200, 'count': res})


class GoodDetailHandler(web.RequestHandler):
    """
    获取商品细节
    """

    @auth_decorator
    async def get(self):
        good_id = self.get_argument('good_id', '')
        good = await objects.get(Goods, id=good_id)
        if good.publisher_id.hex == self.user.id.hex:
            return await self.finish({'status': 200,
                                      'good': {'name': good.name, 'price': good.price, 'inventory': good.inventory,
                                               'comment': good.comment, 'description': good.description}})


class CompleteGood(web.RequestHandler):
    """
    完成交易
    """

    @auth_decorator
    async def get(self):
        order_id = self.get_argument('id')
        try:
            order = await objects.get(Order, id=order_id)
        except Order.DoesNotExist:
            return await self.finish({'code': 404})
        if self.user.id != order.seller_id:
            return await self.finish({'code': 403})
        order.status = False
        order.finish_time = datetime.now()
        await objects.update(order, only=['status', 'finish_time'])
        return await self.finish({'code': 200})
