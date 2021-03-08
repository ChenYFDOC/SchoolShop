import datetime
import random
import re
import hashlib
import jwt
import aiofiles
from tornado import web, websocket
from servers import coder, redis, objects
from .models import *
from .forms import *
from settings import settings
from utils.authLog import auth_decorator
from common_handler import HotsHandler
from apps.shop.models import Order, Goods


class LoginHandler(HotsHandler):
    """
    登录处理handler
    """

    async def get(self):
        await self.render(r'users\login.html', hots=await self.get_hots(redis))

    async def post(self):
        logform = LoginForm(self.request.body_arguments)
        if logform.validate():
            if await redis.get(logform.pic_code.data):
                try:
                    user = await objects.get(Users, phone=logform.phone.data,
                                             password=hashlib.md5(logform.password.data.encode()).hexdigest())
                except Users.DoesNotExist:
                    return await self.finish({'status': 400, 'reason': {'password': '用户名或密码错误！'}})
                else:
                    jwt_token = jwt.encode({
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
                        'user': user.id.hex
                    },
                        settings['cookie_secret'])
                    self.set_cookie('jwt', jwt_token, expires=datetime.datetime.now() + datetime.timedelta(
                        days=7) if logform.remember.data else None, path='/')
                    return await self.finish(
                        {'status': 200, 'next': next_ if (next_ := self.get_argument('next', '')) else None})
            else:
                return await self.finish({'status': 400, 'reason': {'pic_code': '验证码无效！'}})
        else:
            reason = {}
            for field in logform.errors:
                reason[field] = logform.errors[field][0]
            return await self.finish({'status': 400, 'reason': reason})


class LogoutHandler(web.RequestHandler):
    async def get(self):
        self.clear_cookie('jwt')
        self.redirect(self.reverse_url('login'))


class RegistHandler(web.RequestHandler):
    """
    注册处理handler
    """

    async def post(self):
        regform = RegistForm(self.request.arguments)
        if regform.validate():
            id_code = (await redis.get(regform.phone.data)).decode()
            if id_code == regform.phone_code.data:
                try:
                    college = await objects.get(College, College.name == regform.college.data)
                except College.DoesNotExist:
                    return await self.finish({'status': 402, 'reason': {'college': '无效的大学'}})
                user = await objects.create(Users, phone=regform.phone.data,
                                            password=hashlib.md5(regform.password.data.encode()).hexdigest(),
                                            college=college)
                jwt_token = jwt.encode({
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
                    'user': user.id.hex
                },
                    settings['cookie_secret'])
                self.set_cookie('jwt', jwt_token, path='/')
                return await self.finish({'status': 200})
            else:
                return await self.finish({'status': 401, 'reason': {'phone_code': '手机验证码错误！'}})
        else:
            reason = {}
            for field in regform.errors:
                reason[field] = regform.errors[field][0]
            return await self.finish({'status': 400, 'reason': reason})


class MessageHandler(web.RequestHandler):
    """
    短信验证码处理
    """

    async def get(self):
        phone = self.get_argument('phone')
        pic_code = self.get_argument('pic_code')
        if not re.match(r'^1[34578][0-9]{9}$', phone):
            return await self.finish({'status': 402})
        elif await redis.get(pic_code.lower()):
            try:
                await objects.get(Users, phone=phone)
            except Users.DoesNotExist:
                randnum = random.randint(10000, 99999)
                await redis.set(phone, randnum, expire=120)
                # TODO 发送短信
                return await self.finish({'status': 200})
            else:
                return await self.finish({'status': 403})
        else:
            return await self.finish({'status': 401})


class PicCode(web.RequestHandler):
    """
    图片验证码处理
    """

    async def get(self, picCode):
        f, code = coder.getValidCodeImg()
        await redis.set(code.lower(), code, expire=60)
        self.set_header("Content-Type", "image/png")
        await self.finish(f.getvalue())
        f.close()


class ProfileHandler(HotsHandler):

    @auth_decorator
    async def get(self):
        goods = await objects.execute(self.user.goods_set)
        orders_buyer = await objects.prefetch(self.user.order_buyer, Goods.select())
        order_ing = []
        order_end = []
        for order in orders_buyer:
            if order.status:
                order_ing.append(order)
            else:
                order_end.append(order)
        orders_seller = await objects.prefetch(self.user.order_seller, Goods.select())
        sell_ing = []
        sell_end = []
        for order in orders_seller:
            if order.status:
                sell_ing.append(order)
            else:
                sell_end.append(order)
        return await self.render(r'users/profile.html', user_info=self.user, hots=await self.get_hots(redis),
                                 goods=goods, goods_ing=order_ing, goods_end=order_end, sell_ing=sell_ing,
                                 sell_end=sell_end)

    @auth_decorator
    async def patch(self):
        """
        修改账号密码的接口
        :return:
        """
        change_form = ChangeInfo(self.request.arguments)
        if change_form.validate():
            try:
                user = await objects.get(Users, phone=change_form.o_phone.data,
                                         password=(md5_code := hashlib.md5(
                                             change_form.o_password.data.encode()).hexdigest()))
                user.phone = change_form.n_phone.data
                user.password = md5_code
                await objects.update(user, only=('phone', 'password'))
                self.clear_cookie('jwt')
                return await self.finish({'status': 200})
            except Users.DoesNotExist:
                self.clear_cookie('jwt')
                return await self.finish({'status': 403, 'reason': '验证失败'})
        else:
            reason = {}
            for field in change_form.errors:
                reason[field] = change_form.errors[field][0]
            return await self.finish({'status': 401, 'reason': reason})

    @auth_decorator
    async def post(self):
        """
        修改非正式信息的接口
        :return:
        """
        if files := self.request.files:
            file = files['header_pic'][0]
            if not file['content_type'].startswith('image'):
                return await self.finish({'status': 403})
            if o_header := self.user.header:
                file_name = o_header
            else:
                file_name = hashlib.md5((name_list := file['filename'].split('.'))[0].encode()).hexdigest() + '.' + \
                            name_list[1]
            async with aiofiles.open(settings['media_path'] + 'header/' + file_name, mode='wb') as f:
                await f.write(file.body)
            self.user.header = file_name
            await objects.update(self.user, only=('header',))
            return await self.finish({'status': 200})
        # 上面代码是修改头像用的
        info_form = ChangeInformality(self.request.arguments)
        if info_form.validate():
            self.user.nick_name = info_form.nick_name.data
            self.user.email = info_form.email.data
            self.user.trading_address = info_form.trading_address.data
            await objects.update(self.user, only=('nick_name', 'email', 'trading_address'))
            return await self.finish({'status': 200})
        else:
            return await self.finish({'status': 400, 'reason': info_form.errors.popitem()[1][0]})


class ChatWindowHandler(web.RequestHandler):
    @auth_decorator
    async def get(self):
        return await self.render('users/chat.html')


class ChatHandler(websocket.WebSocketHandler):
    pass
