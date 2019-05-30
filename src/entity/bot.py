import peewee

from src.entity.base_entity import BaseEntity


class Bot(BaseEntity):
    name = peewee.CharField(255)
    last_msg_id = peewee.IntegerField(default=0, null=False)
