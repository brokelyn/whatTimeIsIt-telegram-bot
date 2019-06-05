import peewee

from entity.base_entity import BaseEntity
from entity.user import User


class Message(BaseEntity):
    msg_id = peewee.IntegerField(primary_key=True)
    text = peewee.TextField()
    chat_id = peewee.IntegerField()
    user = peewee.ForeignKeyField(model=User)
    time = peewee.DateTimeField()
