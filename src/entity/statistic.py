import peewee

from entity.base_entity import BaseEntity


class Statistic(BaseEntity):
    time = peewee.IntegerField(primary_key=True)
    last_msg_id = peewee.IntegerField(default=0)
