import peewee

from src.entity.base_entity import BaseEntity


class Event(BaseEntity):
    name = peewee.CharField(255)
    start = peewee.TimestampField()  # todo set default
    trigger = peewee.IntegerField()
