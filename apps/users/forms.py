from wtforms import *
from wtforms.validators import *
from wtforms_tornado import Form


class RegistForm(Form):
    phone = StringField(validators=[Length(min=11, max=11, message='无效手机号')])
    password = StringField(validators=[Length(min=5, max=16, message='密码长度在5-16之间')])
    phone_code = StringField()
    college = StringField(validators=[DataRequired(message='请输入大学')])


class LoginForm(Form):
    phone = StringField(validators=[Length(min=11, max=11, message='无效手机号')])
    password = StringField(validators=[Length(min=5, max=16, message='密码长度在5-16之间')])
    pic_code = StringField()
    remember = BooleanField()


class ChangeInfo(Form):
    o_phone = StringField(validators=[Length(min=11, max=11, message='无效手机号')])
    o_password = StringField()
    n_phone = StringField(validators=[Length(min=11, max=11, message='无效手机号')])
    n_password = StringField(validators=[Length(min=5, max=16, message='密码长度在5-16之间')])
    r_password = StringField(validators=[EqualTo(fieldname='n_password', message='两次密码输入不一致！')])


class ChangeInformality(Form):
    nick_name = StringField(validators=[DataRequired(message='请输入昵称')])
    email = StringField(validators=[Email(message='请输入合法邮箱')])
    trading_address = StringField()
