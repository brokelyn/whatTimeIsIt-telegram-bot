import peewee

from entity.base_entity import BaseEntity


class User(BaseEntity):
    id = peewee.IntegerField(primary_key=True)
    username = peewee.CharField(255, null=True)
    first_name = peewee.CharField(255)
    last_name = peewee.CharField(255, null=True)
