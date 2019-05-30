import peewee

from src.entity.base_entity import BaseEntity
from src.entity.user import User


class Message(BaseEntity):
    msg_id = peewee.IntegerField()
    text = peewee.TextField()
    chat_id = peewee.IntegerField(null=False)
    user = peewee.ForeignKeyField(model=User)
    time = peewee.TimestampField()
