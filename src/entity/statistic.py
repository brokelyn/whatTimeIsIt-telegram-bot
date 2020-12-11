import peewee

from entity.base_entity import BaseEntity
from entity.group import Group


class Statistic(BaseEntity):
    id = peewee.AutoField(primary_key=True)
    time = peewee.IntegerField()
    last_msg_id = peewee.IntegerField(default=0)
    group = peewee.ForeignKeyField(model=Group)
