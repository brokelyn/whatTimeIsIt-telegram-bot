import peewee

from src.entity.base_entity import BaseEntity


class User(BaseEntity):
    username = peewee.CharField(255, null=False, primary_key=True, unique=True)
    first_name = peewee.CharField(255)
    last_name = peewee.CharField(255)
