from peewee import *
from servers import db
import uuid


class College(Model):
    name = CharField(max_length=16)

    class Meta:
        database = db
        table_name = 'school'


class Users(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    phone = CharField(max_length=11)
    password = CharField()
    email = CharField(null=True)
    nick_name = CharField(max_length=8, null=True)
    header = CharField(null=True)
    trading_address = CharField(null=True)
    college = ForeignKeyField(College, on_delete='cascade')

    class Meta:
        database = db


if __name__ == '__main__':
    with db.allow_sync():
        db.connect()
        db.create_tables([Users])
