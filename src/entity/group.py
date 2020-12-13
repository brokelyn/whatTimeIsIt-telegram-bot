import peewee

from entity.base_entity import BaseEntity


class Group(BaseEntity):
    id = peewee.BigIntegerField(primary_key=True)
    title = peewee.TextField()
    auto_events = peewee.BooleanField(default=False)
    auto_ban = peewee.BooleanField(default=False)
    timezone = peewee.TextField(null=True)
    invite_link = peewee.TextField(null=True)
