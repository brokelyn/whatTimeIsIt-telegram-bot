import peewee

from src.entity.base_entity import BaseEntity
from src.entity.user import User
from src.entity.statistic import Statistic


class Score(BaseEntity):
    user = peewee.ForeignKeyField(model=User)
    points = peewee.IntegerField(null=False, default=0)
    board = peewee.ForeignKeyField(model=Statistic, null=False)
