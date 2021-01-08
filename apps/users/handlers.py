import random
import re
import hashlib
from tornado import web
from servers import coder, redis, objects
from .models import Users
from .forms import RegistForm


class LoginHandler(web.RequestHandler):
    async def get(self, *args, **kwargs):
        await self.render(r'users\login.html')


class RegistHandler(web.RequestHandler):
    async def post(self):
        regform = RegistForm(self.request.arguments)
        if regform.validate():
            id_code = await redis.get(regform.phone.data)
            if id_code == regform.phone_code.data:
                await objects.create(Users, phone=regform.phone.data,
                                     password=hashlib.md5(regform.password.data).hexdigest(),
                                     college=regform.college.data)
                return self.finish({'status': 200})
        else:
            reason = {}
            for field in regform.errors:
                reason[field] = regform.errors[field][0]
            return self.finish({'status': 400, 'reason': reason})


class MessageHandler(web.RequestHandler):
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

    async def get(self, *args, **kwargs):
        f, code = coder.getValidCodeImg()
        await redis.set(code.lower(), code, expire=60)
        self.set_header("Content-Type", "image/png")
        await self.finish(f.getvalue())
        f.close()
