import peewee

from src.entity.base_entity import BaseEntity
from src.entity.event import Event
from src.entity.user import User


class Score(BaseEntity):
    user = peewee.ForeignKeyField(model=User, null=False, primary_key=True)
    event = peewee.ForeignKeyField(model=Event, null=False, primary_key=True)
    points = peewee.IntegerField(default=0)
