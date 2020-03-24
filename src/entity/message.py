import peewee

from entity.base_entity import BaseEntity
from entity.user import User


class Message(BaseEntity):
    id = peewee.AutoField(primary_key=True)
    msg_id = peewee.BigIntegerField()
    text = peewee.TextField()
    chat_id = peewee.BigIntegerField()
    user = peewee.ForeignKeyField(model=User)
    time = peewee.DateTimeField()
