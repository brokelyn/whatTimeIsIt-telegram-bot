import peewee

from entity.base_entity import BaseEntity


class Group(BaseEntity):
    id = peewee.BigIntegerField(primary_key=True)
    title = peewee.TextField()
    auto_events = peewee.BooleanField(default=False)
    violation_action = peewee.CharField(16, default="ban")
    timezone = peewee.TextField(null=True)
    invite_link = peewee.TextField(null=True)
