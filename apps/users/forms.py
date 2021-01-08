from wtforms import *
from wtforms.validators import *
from wtforms_tornado import Form


class RegistForm(Form):
    phone = StringField(validators=[Length(min=11, max=11, message='无效手机号')])
    password = StringField(validators=[Length(min=5, max=16, message='密码长度在5-16之间')])
    phone_code = StringField()
    college = StringField()
