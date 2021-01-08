from peewee import *
from servers import db


class Users(Model):
    id = UUIDField(primary_key=True)
    phone = CharField(max_length=11)
    password = CharField()
    email = CharField(null=True)
    nick_name = CharField(max_length=8, null=True)
    college = CharField()

    class Meta:
        database = db


if __name__ == '__main__':
    with db.allow_sync():
        db.connect()
        db.create_tables([Users])
