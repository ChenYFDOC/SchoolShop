from wtforms import *
from wtforms.validators import *
from wtforms_tornado import Form


class Good(Form):
    price = FloatField(validators=[DataRequired(message='必须输入价格'), NumberRange(min=0, message='非法价格范围')])
    name = StringField(validators=[DataRequired(message='必须输入名称'), Length(max=32, message='名称长度最大为32')])
    inventory = IntegerField(default=1)
    comment = StringField(validators=[DataRequired(message='请输入大致描述'), Length(max=150, message='描述限定在150个字')])
    description = StringField()
