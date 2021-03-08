import uuid
from peewee import *
from servers import db
import apps.users.models as users_models
from datetime import datetime


class Goods(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    price = FloatField()
    publisher = ForeignKeyField(users_models.Users)
    status = IntegerField(default=0, choices=((0, '已发布'), (1, '交易中'), (2, '交易结束'), (3, '已下架')))
    name = CharField(max_length=32)
    comment = CharField(max_length=150)
    description = TextField(null=True)
    inventory = IntegerField(default=1)
    publish_time = DateField(default=datetime.now)
    edit_time = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class Order(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    good = ForeignKeyField(Goods, on_delete='cascade')
    buyer = ForeignKeyField(users_models.Users, on_delete='cascade', backref='order_buyer')
    status = BooleanField(default=True)
    seller = ForeignKeyField(users_models.Users, on_delete='cascade', backref='order_seller')
    finish_time = DateTimeField(null=True)

    class Meta:
        database = db


if __name__ == '__main__':
    with db.allow_sync():
        db.connect()
        db.create_tables([Goods, Order])
