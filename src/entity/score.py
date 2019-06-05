import peewee

from entity.base_entity import BaseEntity
from entity.user import User
from entity.statistic import Statistic


class Score(BaseEntity):
    user = peewee.ForeignKeyField(model=User)
    points = peewee.IntegerField(default=0)
    stat = peewee.ForeignKeyField(model=Statistic)
    date = peewee.IntegerField(default=0)
