import peewee

from entity.base_entity import BaseEntity
from entity.group import Group


class Event(BaseEntity):
    time = peewee.IntegerField()
    group = peewee.ForeignKeyField(model=Group)

    class Meta:
        primary_key = peewee.CompositeKey('time', 'group')
