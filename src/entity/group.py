import peewee

from entity.base_entity import BaseEntity


class Group(BaseEntity):
    id = peewee.BigIntegerField(primary_key=True)
    title = peewee.TextField()
    invite_link = peewee.TextField(null=True)
