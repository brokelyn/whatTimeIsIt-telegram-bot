import peewee

from entity.base_entity import BaseEntity


class Statistic(BaseEntity):
    time = peewee.IntegerField(null=False, primary_key=True)
    last_msg_id = peewee.IntegerField(null=False, default=0)
