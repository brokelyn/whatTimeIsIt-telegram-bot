import peewee

from entity.base_entity import BaseEntity


class Event(BaseEntity):
    time = peewee.IntegerField(primary_key=True)
    chat_id = peewee.IntegerField()
