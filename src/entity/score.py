import peewee

from src.entity.base_entity import BaseEntity
from src.entity.event import Event
from src.entity.user import User


class Score(BaseEntity):
    user = peewee.ForeignKeyField(model=User, null=False)
    event = peewee.ForeignKeyField(model=Event, null=False)
    points = peewee.IntegerField(default=0)
