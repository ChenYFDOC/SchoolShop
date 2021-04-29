import jwt
import datetime
from settings import settings
from servers import objects
from apps.users.models import Users
from tornado.websocket import WebSocketHandler


def auth_decorator(func):
    """
    登录验证装饰器，没登陆会跳转到登陆界面并指向当前界面
    :param func:
    :return:
    """

    async def auth_log(self, *args, **kwargs):
        token = self.get_cookie(name='jwt')
        try:
            user_info = jwt.decode(token, key=settings['cookie_secret'], leeway=datetime.timedelta(hours=8),
                                   algorithms=["HS256"])
            user = await objects.get(Users, id=user_info['user'])
            self.user = user
        except:
            self.set_status(302)
            self.set_header('Location', self.get_login_url() + f'next={self.request.uri}')
            return await self.finish()

        return await func(self, *args, **kwargs)

    return auth_log


def auth_ws(func):
    """
    websocket验证装饰器
    :param func:
    :return:
    """

    async def auth_log(self, *args, **kwargs):
        token = self.get_cookie(name='jwt')
        try:
            user_info = jwt.decode(token, key=settings['cookie_secret'], leeway=datetime.timedelta(hours=8),
                                   algorithms=["HS256"])
            user = await objects.get(Users, id=user_info['user'])
            self.user = user
        except:
            if isinstance(self, WebSocketHandler):
                return self.close()
            self.set_status(404)
            return await self.finish({'code': 404})

        return await func(self, *args, **kwargs)

    return auth_log
